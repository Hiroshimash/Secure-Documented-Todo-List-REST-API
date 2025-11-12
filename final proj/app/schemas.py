# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoOut(TodoBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    class Config:
        orm_mode = True
