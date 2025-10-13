from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin

class UserCRUD:


    @staticmethod
    def create_user(db: Session, user: UserCreate):
        existing_User = db.query(User).filter(User.email == user.email).first()
        if existing_User:
            return None

        new_user = User(username=user.username, email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print("User created successfully")
        return new_user

    @staticmethod
    def login_user(db: Session, user: UserLogin):
        user = db.query(User).filter(User.email == user.email).first()
        if user and user.password == user.password:
            return user
        else:
            return None

    @staticmethod
    def check_admin_status(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        return user is not None and user.is_admin # ✅ Защита от None

