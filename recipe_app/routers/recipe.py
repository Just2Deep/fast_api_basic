from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..schemas import RecipePost, RecipeOut
from ..models import Recipe
from ..database import get_db
from ..oauth2 import get_current_user, optional_oauth2_scheme


router = APIRouter(prefix="/recipes", tags=["Recipe"])


@router.get("/", response_model=List[RecipeOut])
def get_all_posts(db: Session = Depends(get_db)) -> List[RecipeOut]:
    """Get All Published Recipes

    Args:
        db (Session, optional): Intiliasing db instance. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if not found

    Returns:
        List[Recipes]: list of recipes
    """
    if recipes := db.query(Recipe).filter_by(is_publish=True).all():
        return recipes

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No Recipes Present"
    )


@router.post("/", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
def create_a_post(
    recipe_data: RecipePost,
    token: str = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
) -> RecipeOut:
    """Create a new recipe

    RecipePost
    **name**: str
    **description**: str
    **num_of_servings**: int
    **cook_time**: int
    **directions**: str

    Args:
        recipe_data (RecipePost): User Input
        token (str, optional): access token. Defaults to Depends(optional_oauth2_scheme).
        db (Session, optional): db instance. Defaults to Depends(get_db).

    Raises:
        HTTPException: 403

    Returns:
        RecipeOut: Recipe
    """
    if user := get_current_user(token=token, db=db):
        new_recipe = Recipe(user_id=user.id, **recipe_data.dict())

        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

        return new_recipe

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/{recipe_id}", response_model=RecipeOut, status_code=status.HTTP_200_OK)
def get_one_recipe(
    recipe_id: int,
    token: str = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
) -> RecipeOut:
    """Get a single recipe

    Args:
        recipe_id (int): Id of the recipe to fetch
        token (str, optional): access token. Defaults to Depends(optional_oauth2_scheme).
        db (Session, optional): db instance. Defaults to Depends(get_db).

    Raises:
        HTTPException: 403 if not authorised
        HTTPException: 404 if not found

    Returns:
        RecipeOut: Recipe
    """
    if recipe := db.query(Recipe).filter_by(id=recipe_id).first():
        current_user = get_current_user(token=token, db=db)
        if recipe.is_publish == True or (
            recipe.is_publish == False
            and current_user
            and current_user.id == recipe.user_id
        ):
            return recipe
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access not allowed"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
    )


@router.put("/{recipe_id}", response_model=RecipeOut, status_code=status.HTTP_200_OK)
def update_a_recipe(
    recipe_id: int,
    recipe_data: RecipePost,
    token: str = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
) -> RecipeOut:
    """Update a recipe using put

    RecipePost
    **name**: str
    **description**: str
    **num_of_servings**: int
    **cook_time**: int
    **directions**: str

    Args:
        recipe_id (int): id of the recipe to update
        recipe_data (RecipePost): User input
        token (str, optional): access token. Defaults to Depends(optional_oauth2_scheme).
        db (Session, optional): db instance. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if not found
        HTTPException: 403 if not authorised

    Returns:
        RecipeOut: Recipe after update
    """
    recipe_query = db.query(Recipe).filter_by(id=recipe_id)
    recipe_db = recipe_query.first()
    if recipe := recipe_db:
        current_user = get_current_user(token=token, db=db)
        if current_user and current_user.id == recipe.user_id:
            recipe_query.update(recipe_data.dict(), synchronize_session=False)
            db.commit()
            db.refresh(recipe)

            return recipe
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access not allowed"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
    )


@router.delete(
    "/{recipe_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
def delete_a_recipe(
    recipe_id: int,
    token: str = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
) -> None:
    """Delete a recipe

    Args:
        recipe_id (int): id of the recipe to delete
        token (str, optional): access token. Defaults to Depends(optional_oauth2_scheme).
        db (Session, optional): db instance. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if not found
        HTTPException: 403 if not authorised

    Returns:
        None
    """
    recipe_query = db.query(Recipe).filter_by(id=recipe_id)
    recipe_db = recipe_query.first()
    if recipe := recipe_db:
        current_user = get_current_user(token=token, db=db)
        if current_user and current_user.id == recipe.user_id:
            db.delete(recipe)
            db.commit()

            return {}
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access not allowed"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
    )


@router.put(
    "/{recipe_id}/publish", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
def publish_a_recipe(
    recipe_id: int,
    token: str = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
) -> None:
    """Publish a recipe

    Args:
        recipe_id (int): id of the recipe to publish
        token (str, optional): access token. Defaults to Depends(optional_oauth2_scheme).
        db (Session, optional): db instance. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if not found
        HTTPException: 403 if not authorised

    Returns:
        None
    """
    recipe_query = db.query(Recipe).filter_by(id=recipe_id)
    recipe_db = recipe_query.first()
    if recipe := recipe_db:
        current_user = get_current_user(token=token, db=db)
        if current_user and current_user.id == recipe.user_id:
            recipe.is_publish = True
            db.add(recipe)
            db.commit()

            return {}
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access not allowed"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
    )


@router.delete(
    "/{recipe_id}/publish", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
def unpublish_a_recipe(
    recipe_id: int,
    token: str = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
) -> None:
    """Unpublish a recipe

    Args:
        recipe_id (int): id of the recipe to unpublish
        token (str, optional): access token. Defaults to Depends(optional_oauth2_scheme).
        db (Session, optional): db instance. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if not found
        HTTPException: 403 if not authorised

    Returns:
        None
    """
    recipe_query = db.query(Recipe).filter_by(id=recipe_id)
    recipe_db = recipe_query.first()
    if recipe := recipe_db:
        current_user = get_current_user(token=token, db=db)
        if current_user and current_user.id == recipe.user_id:
            recipe.is_publish = False
            db.add(recipe)
            db.commit()

            return {}
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access not allowed"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
    )
