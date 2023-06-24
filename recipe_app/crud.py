from sqlalchemy.orm import Session

from . import models, schemas


def get_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_recipes_db(db: Session):
    return db.query(models.Recipe).filter(models.Recipe.is_publish == True).all()


def add_new_recipe(db: Session, recipe: schemas.RecipePost):
    print(**recipe.dict())
    db_recipe = models.Recipe(**recipe.dict())

    print(recipe)
    db.add(recipe)
    db.commit()
    db_recipe = db.refresh(recipe)

    return db_recipe
