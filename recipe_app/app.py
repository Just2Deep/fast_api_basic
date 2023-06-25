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


# @app.get("/recipes", status_code=status.HTTP_200_OK)
# def get_all_recipes(response: Response, db: Session = Depends(get_db)):
#     recipes = []

#     return {"data": recipes}


# @app.post("/recipes", status_code=status.HTTP_201_CREATED)
# def post_new_recipe(recipe: RecipePost, db: Session = Depends(get_db)):
#     return []


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
