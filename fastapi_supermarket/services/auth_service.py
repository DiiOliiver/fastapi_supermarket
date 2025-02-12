from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_oauth2form import T_OAuth2Form
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from fastapi_supermarket.models import User
from fastapi_supermarket.schemas.token_schema import Token


def generate_token(
    session: T_Session,
    form_data: T_OAuth2Form,
) -> Token:
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
    return Token(access_token=access_token, token_type='Bearer')


def refresh_token(current_user: T_CurrentUser) -> Token:
    new_token = create_access_token(data_payload={'sub': current_user.email})
    return Token(access_token=new_token, token_type='Bearer')
