from tempfile import template

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends
from fastapi import Request

from sqlalchemy.orm import Session
from sqlalchemy import text


from database import engine, get_db

app = FastAPI()


template = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
async def root(request: Request):
    return template.TemplateResponse("home.html", {"request": request})







if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            print("✅ Подключение успешно!")
            print("🧩 Версия PostgreSQL:", result.scalar())
    except Exception as e:
        print(f"Error connecting to database: {e}")

    uvicorn.run(app, host="127.0.0.1", port=8000)