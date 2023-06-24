from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from .schemas import TokenData

SECRET_KEY = "0f3a898351a48a59da1ab2e4ec13f63cc825ff7a677cb9921ff2e2f15fad2346"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)

        if id := payload.get("user_id"):
            return TokenData(id=id)
        raise credentials_exception
    except JWTError:
        raise credentials_exception


def get_current_user():
    return
