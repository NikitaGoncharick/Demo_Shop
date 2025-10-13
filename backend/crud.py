from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

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
