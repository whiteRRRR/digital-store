from typing import Annotated
from jwt import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import (
    HTTPException,
    status,
    Form,
    Depends
)
from .utils import (
    verify_password,
    password_in_hash,
    decode_auth_token
)

from .schemas import (
    UserInDataBase,
    UserBase
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

alex = UserInDataBase(
    username="alex",
    first_name="Alex",
    last_name="Mercedes",
    email="alex@gmail.com",
    phone_number="+447911123456",
    password=password_in_hash("alex1")
)


john = UserInDataBase(
    username="John",
    first_name="John",
    last_name="BMW",
    email="john@gmail.com",
    phone_number="+447911123456",
    password=password_in_hash("john1")
)


db: dict[str, UserInDataBase] = {
    john.username: john,
    alex.username: alex,
}


def get_user_in_db(database, username):
    if username in database:
        user_info = database[username]
        return user_info


def get_token_payload(token: Annotated[str | bytes, Depends(oauth2_scheme)]) -> UserBase:

    try:
        payload = decode_auth_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return payload


def get_current_user(payload: dict = Depends(get_token_payload)) -> UserBase:
    username = payload.get("sub")
    user = get_user_in_db(db, username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)"
        )
    return user


def get_active_user(user: Annotated[UserBase, Depends(get_current_user)]) -> UserBase:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User Inactive"
        )
    return user


def validate_user_authenticated(username: str = Form(), password: str = Form()):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or login",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = get_user_in_db(db, username)
    if not user:
        raise exception
    if not verify_password(password, user.password):
        raise exception
    return user










