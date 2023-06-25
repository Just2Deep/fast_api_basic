from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas import Token
from ..models import User
from ..database import get_db
from ..utils import verify_password
from ..oauth2 import create_access_token


router = APIRouter(tags=["Authentication"])


@router.post("/token", response_model=Token)
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
