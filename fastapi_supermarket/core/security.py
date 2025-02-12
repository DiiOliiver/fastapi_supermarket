from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from pwdlib import PasswordHash
from sqlalchemy import select

from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.core.settings import Settings
from fastapi_supermarket.models import User

settings = Settings()

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_password_hash(password: str) -> str:  # pragma: no cover
    return pwd_context.hash(password)


def verify_password(
    plain_password: str, hashed_password: str
) -> bool:  # pragma: no cover
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data_payload: dict) -> str:
    to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('America/Manaus')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    session: T_Session,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email: str = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user_db = session.scalar(
        select(User).where(
            User.deleted_at.is_(None) & (User.email == subject_email)
        )
    )

    if not user_db:
        raise credentials_exception

    return user_db
