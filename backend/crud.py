from symtable import Class

from sqlalchemy.orm import Session

from models import User, Product
from schemas import UserCreate, UserLogin, ProductCreate, ProductEdit

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


class ProductCRUD:

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate):
        db_product = Product(
            name=product_data.name,
            price=product_data.price,
            quantity=product_data.quantity,
            description=product_data.description,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    @staticmethod
    def get_all_products(db: Session):

        all_products = db.query(Product).all()
        products_data = []

        for product in all_products:
            products_data.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "description": product.description
            })

        return products_data

    @staticmethod
    def edit_product(db: Session, product_data: ProductEdit):
        product = db.query(Product).filter(Product.id == product_data.id).first()
        if product:
            product.name = product_data.name
            product.price = product_data.price
            product.quantity = product_data.quantity
            product.description = product_data.description

            db.commit()
            db.refresh(product)
            return product
        else:
            return None

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        else:
            return False


