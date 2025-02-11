from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_supermarket.core.database import get_session
from fastapi_supermarket.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from fastapi_supermarket.models import User
from fastapi_supermarket.schemas.token_schema import Token

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(
            User.deleted_at.is_(None)
            & (
                (User.email == form_data.username)
                | (User.password == get_password_hash(form_data.password))
            )
        )
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Authentication credentials is invalid.',
        )
    access_token = create_access_token(data_payload={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
