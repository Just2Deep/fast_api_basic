from fastapi import FastAPI, Response, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import RecipePost, UserCreate, UserOut, Token, UserLogin
from .models import Recipe, User
from .database import get_db
from .utils import hash_password, verify_password
from .oauth2 import create_access_token
from sqlalchemy.orm import Session

app = FastAPI()


@app.post("/login", response_model=Token)
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    if not (
        user := db.query(User).filter(User.email == user_credentials.username).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )
    if valid := verify_password(user_credentials.password, user.password):
        access_token = create_access_token({"user_id": user.id})

        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Credentials",
    )


@app.get("/recipes", status_code=status.HTTP_200_OK)
def get_all_recipes(response: Response, db: Session = Depends(get_db)):
    recipes = []

    return {"data": recipes}


@app.post("/recipes", status_code=status.HTTP_201_CREATED)
def post_new_recipe(recipe: RecipePost, db: Session = Depends(get_db)):
    return []


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    if user_data := db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            detail=f"user with email {user.email} is already present",
        )

    if user_data := db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            detail=f"user with username {user.username} is already present",
        )

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @app.get("/recipes/{recipe_id}", status_code=status.HTTP_200_OK)
# def get_one_recipe(recipe_id: int, response: Response, db: Session = Depends(get_db)):
#     if recipe := next(
#         (recipe for recipe in recipe_list if recipe.id == recipe_id), None
#     ):
#         return recipe.data

#     response.status_code = status.HTTP_404_NOT_FOUND
#     return {"msg": "recipe does not exist"}


# @app.put("/recipes/{recipe_id}", status_code=status.HTTP_200_OK)
# def modify_recipe(
#     recipe_id: int, data: RecipePost, response: Response, db: Session = Depends(get_db)
# ):
#     if recipe := next(
#         (recipe for recipe in recipe_list if recipe.id == recipe_id), None
#     ):
#         recipe.name = data.name
#         recipe.description = data.description
#         recipe.num_of_servings = data.num_of_servings
#         recipe.cook_time = data.cook_time
#         recipe.directions = data.directions

#         return recipe.data

#     response.status_code = status.HTTP_404_NOT_FOUND
#     return {"msg": "recipe does not exist"}


# @app.put("/recipes/{recipe_id}/publish", status_code=status.HTTP_204_NO_CONTENT)
# def publish_recipe(recipe_id: int, response: Response, db: Session = Depends(get_db)):
#     if recipe := next(
#         (recipe for recipe in recipe_list if recipe.id == recipe_id), None
#     ):
#         recipe.is_publish = True
#         return {}

#     response.status_code = status.HTTP_404_NOT_FOUND
#     return {"msg": "recipe does not exist"}


# @app.delete("/recipes/{recipe_id}/publish", status_code=status.HTTP_204_NO_CONTENT)
# def unpublish_recipe(recipe_id: int, response: Response, db: Session = Depends(get_db)):
#     if recipe := next(
#         (recipe for recipe in recipe_list if recipe.id == recipe_id), None
#     ):
#         recipe.is_publish = False
#         return {}

#     response.status_code = status.HTTP_404_NOT_FOUND
#     return {"msg": "recipe does not exist"}
