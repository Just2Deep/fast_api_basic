from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class RecipePost(BaseModel):
    name: str
    description: str
    num_of_servings: int
    cook_time: int
    directions: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None