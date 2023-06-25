from typing import Union
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..schemas import UserOut, UserCreate, UserOutMe
from ..models import User
from ..database import get_db
from ..utils import hash_password
from ..oauth2 import get_current_user, optional_oauth2_scheme

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
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


@router.get(
    "/{username}",
    response_model=Union[UserOutMe, UserOut],
)
def get_user(
    username: str,
    db: Session = Depends(get_db),
    token: str = Depends(optional_oauth2_scheme),
):
    if user := db.query(User).filter(User.username == username).first():
        current_user = get_current_user(token, db)
        if not current_user or current_user.username != username:
            return UserOut(id=user.id, username=user.username)
        return UserOutMe(
            id=current_user.id, username=current_user.username, email=current_user.email
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"user {username} does not exist"
    )
