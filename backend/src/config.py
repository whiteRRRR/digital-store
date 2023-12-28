from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent


class AuthJWT(BaseModel):
    public_key: Path = BASE_DIR / "certs" / "public_key.pem"
    private_key: Path = BASE_DIR / "certs" / "private_key.pem"
    algorithm: str = "RS256"
    access_token_expires_in: int = 3


class Settings(BaseModel):
    jwt_auth: AuthJWT = AuthJWT()


settings = Settings()