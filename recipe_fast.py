from fastapi import FastAPI, status, Response
from pydantic import BaseModel


app = FastAPI()

recipe_list = [
    {"id": 1, "name": "Egg Salad", "description": "This is a lovely egg salad recipe."},
    {
        "id": 2,
        "name": "Tomato Pasta",
        "description": "This is a lovely tomato pasta recipe.",
    },
]


class Recipe(BaseModel):
    id: int | None
    name: str
    description: str


@app.get("/")
def home():
    return {"hello": "Welcome Home"}


@app.get("/recipes", status_code=status.HTTP_200_OK)
def recipes():
    return {"data": recipe_list}


@app.get("/recipes/{recipe_id}", status_code=status.HTTP_200_OK)
def recipes(recipe_id: int, response: Response):
    if recipe := [recipe for recipe in recipe_list if recipe["id"] == recipe_id]:
        return {"data": recipe}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": f"no recipe with id {recipe_id}"}


@app.post("/recipes", status_code=status.HTTP_201_CREATED)
def new_recipe(recipe_data: Recipe):
    recipe_id = len(recipe_list) + 1
    recipe_name = recipe_data.name
    recipe_description = recipe_data.description

    recipe = {"id": recipe_id, "name": recipe_name, "description": recipe_description}
    recipe_list.append(recipe)

    return {"data": recipe}


@app.put("/recipes/{recipe_id}", status_code=status.HTTP_200_OK)
def update_recipes(recipe_id: int, recipe_data: Recipe, response: Response):
    if recipe := next(
        (recipe for recipe in recipe_list if recipe["id"] == recipe_id), None
    ):
        recipe["name"] = recipe_data.name
        recipe["description"] = recipe_data.description

        return {"data": recipe}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "recipe not found"}


@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_recipes(recipe_id: int, response: Response):
    if recipe := next(
        (recipe for recipe in recipe_list if recipe["id"] == recipe_id), None
    ):
        recipe_list.remove(recipe)
        return

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "recipe not found"}
