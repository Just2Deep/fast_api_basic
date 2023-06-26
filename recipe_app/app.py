from fastapi import FastAPI
from .routers import auth, user, recipe

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(recipe.router)


@app.get("/")
def root():
    return {"message": "Hello Applications!"}
