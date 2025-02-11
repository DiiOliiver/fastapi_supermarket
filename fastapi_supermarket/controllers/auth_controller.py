from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fastapi_supermarket.annotaded.T_OAuth2Form import T_OAuth2Form
from fastapi_supermarket.annotaded.T_Session import T_Session
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
    session: T_Session,
    form_data: T_OAuth2Form,
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
