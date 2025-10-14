from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserStatus(BaseModel):
    status: str

class Product(BaseModel):
    name: str
    price: float
    quantity: int
    description: str