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

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int