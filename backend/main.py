from os import access
from tempfile import template

import uvicorn
from schemas import UserCreate, UserLogin
from crud import UserCRUD
from fastapi import FastAPI, Form, HTTPException, status, requests
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import ValidationError

from jose import jwt, JWTError


from database import engine, get_db
from auth import create_access_token, decode_token
from config import  ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models import Base

# 🚀 Создаем таблицы в БД
Base.metadata.create_all(bind=engine)
app = FastAPI()


template = Jinja2Templates(directory="../frontend/templates")


@app.get("/")
async def root(request: Request):
    return template.TemplateResponse("home.html", {"request": request})

# Веб-интерфейс
@app.get("/register")
async def register_page(request: Request):
    return template.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_comand(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        user_data = UserCreate(username=username, email=email, password=password) #Валидация данных
    except Exception as e:
        return {"error": str(e)}

    new_user = UserCRUD.create_user(db, user_data) #Попытка регистрации

    if not new_user:
        print("User already exists")

    #return JSONResponse({"User created successfully": "1111"})
    return RedirectResponse(url="/login", status_code=303)


# Веб-интерфейс
@app.get("/login")
async def login_page(request: Request):
    return template.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_command(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db) ):
    try:
        login_data = UserLogin(email=email, password=password) #Валидация данных
    except Exception as e:
        return RedirectResponse(url="/login?error=invalid_credentials", status_code=303)


    user = UserCRUD.login_user(db, login_data) #Попытка логина
    if not user:
        return RedirectResponse(url="/login?error=invalid_credentials", status_code=303)

    # Создаем токен
    access_token = create_access_token(data={"sub": user.username})

    redirect = RedirectResponse(url="/login", status_code=303)
    redirect.set_cookie(key="access_token", value=access_token, httponly=True, max_age= ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    #return JSONResponse({"username" : user.username, "email": user.email, "access_token": access_token})
    return redirect



# Проверки
# ✅ Зависимость для получения текущего пользователя
async def get_current_user(request: Request, db: Session = Depends(get_db)):

    access_token = request.cookies.get("access_token") # Достаем токен из кук
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")  # ✅ Только исключения

    try:
        username = decode_token(access_token)
        return username
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Operation")


# ✅ Зависимость для проверки админа
async def require_admin(username: str = Depends(get_current_user), db: Session = Depends(get_db)):

    admin_status = UserCRUD.check_admin_status(db, username)
    if not admin_status:
        raise HTTPException(status_code=403, detail="No admin permission ")

    return username


# Администрация, защищенные эндпоинты
@app.get("/admin/dashboard")
async def admin_dashboard(request: Request, admin_user: str = Depends(require_admin)):
        # Блок выполнится только в случае прохождения проверки через Depends
        return template.TemplateResponse("admin_dashboard.html", {"request": request})








if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            print("✅ Подключение установлено")
            print("🧩 Версия PostgreSQL:", result.scalar())
    except Exception as e:
        print(f"Error connecting to database: {e}")

    uvicorn.run(app, host="127.0.0.1", port=8000)