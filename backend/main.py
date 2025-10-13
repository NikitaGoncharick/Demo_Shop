from tempfile import template

import uvicorn
from schemas import UserCreate
from crud import UserCRUD
from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy import text


from database import engine, get_db
from models import Base

# 🚀 Создаем таблицы в БД
Base.metadata.create_all(bind=engine)
app = FastAPI()


template = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
async def root(request: Request):
    return template.TemplateResponse("home.html", {"request": request})


@app.post("/register")
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        userData = UserCreate(username=username, email=email, password=password)
    except Exception as e:
        return {"error": str(e)}

    new_user = UserCRUD.create_user(db, userData)

    if not new_user:
        print("User already exists")

    return "User created successfully"




#2. Разные зависимости для проверки ролей
# Базовая проверка авторизации
# def check_auth(request: Request):
#     # проверка JWT токена
#     return user
#
# # Проверка что пользователь - админ
# def check_admin(user: User = Depends(check_auth)):
#     if not user.is_admin:
#         raise HTTPException(403, "Admin access required")
#     return user

#3. Использование в эндпоинтах
# Для пользователей
# @app.get("/shop/cart")
# async def user_cart(user: User = Depends(check_auth)):
#     return {"cart": user.cart}
#
# # Для админов
# @app.get("/admin/dashboard")
# async def admin_dashboard(admin: User = Depends(check_admin)):
#     return {"stats": "admin_data"}







if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            print("✅ Подключение установлено")
            print("🧩 Версия PostgreSQL:", result.scalar())
    except Exception as e:
        print(f"Error connecting to database: {e}")

    uvicorn.run(app, host="127.0.0.1", port=8000)