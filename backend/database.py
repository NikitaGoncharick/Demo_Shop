from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# 🔗 Подключение к PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1@localhost:5432/Store_Database" #имя.пароль(как при созднии postgress).порт.название бд

# 🚀 Создаем движок БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True # ✅ проверяет соединение перед использованием
)

# 🎭 Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🏗️ Базовый класс для моделей
base = declarative_base()

# 🔄 Dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()