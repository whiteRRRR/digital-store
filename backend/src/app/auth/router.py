from datetime import datetime, timedelta
from typing import Dict, Any

from fastapi import (
    APIRouter,
    status,
    Depends
)
from fastapi.encoders import jsonable_encoder
from fastapi.security import (
    OAuth2PasswordBearer,
)
from starlette.authentication import BaseUser

from .utils import (
    password_in_hash,
    encode_auth_token,
)
from .schemas import (
    UserInDataBase,
    UserBase,
    Token,
)
from .dependencies import (
    validate_user_authenticated,
    get_active_user,
)


router = APIRouter(tags=["Auth"], prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/login", response_model=Token)
async def authenticate_user(
        user: UserInDataBase = Depends(validate_user_authenticated)
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }

    token = encode_auth_token(jwt_payload)

    return Token(access_token=token, token_type="Bearer")


@router.get("/users/me", response_model=UserBase)
async def read_user(user: UserBase = Depends(get_active_user)):
    print(user)
    return jsonable_encoder(user)






