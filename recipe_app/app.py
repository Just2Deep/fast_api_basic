from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import RecipePost, UserCreate, UserOut, Token
from .models import Recipe, User
from .database import get_db
from .utils import hash_password, verify_password
from .oauth2 import create_access_token
from sqlalchemy.orm import Session
from .routers import auth, user, recipe

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(recipe.router)


@app.get("/")
def root():
    return {"message": "Hello Applications!"}
