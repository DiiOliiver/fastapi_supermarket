from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:  # pragma: no cover
    return pwd_context.hash(password)


def verify_password(
    plain_password: str, hashed_password: str
) -> bool:  # pragma: no cover
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data_payload: dict) -> dict:
    to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('America/Manaus')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
