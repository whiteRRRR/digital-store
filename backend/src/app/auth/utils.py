from datetime import timedelta, datetime
import bcrypt
import jwt
from backend.src.config import settings


def encode_auth_token(
        payload: dict,
        private_key: str = settings.jwt_auth.private_key.read_text(),
        algorithm: str = settings.jwt_auth.algorithm,
        expire_minutes: int = settings.jwt_auth.access_token_expires_in,
        expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if not expire_timedelta:
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    else:
        expire = datetime.utcnow() + expire_timedelta
    to_encode.update({
        "exp": expire,
        "iat": now
    })
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_auth_token(
        token: str | bytes,
        public_key: str = settings.jwt_auth.public_key.read_text(),
        algorithm: str = settings.jwt_auth.algorithm
):
    print(algorithm)
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return decoded


def password_in_hash(password: str) -> bytes:
    password_bytes: bytes = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)


def verify_password(password: str, hash_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password)


