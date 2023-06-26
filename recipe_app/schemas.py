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
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserOutPost(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserOutMe(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RecipeOut(RecipePost):
    id: int
    author: UserOutPost
    is_publish: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
