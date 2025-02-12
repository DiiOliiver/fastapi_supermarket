from http import HTTPStatus

from fastapi import APIRouter

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_oauth2form import T_OAuth2Form
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.schemas.token_schema import Token
from fastapi_supermarket.services.auth_service import (
    generate_token,
    refresh_token,
)

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
) -> Token:
    """Gera token."""
    return generate_token(session, form_data)


@router.post('/token/refresh', status_code=HTTPStatus.OK, response_model=Token)
def refresh_access_token(current_user: T_CurrentUser) -> Token:
    """Gera um novo token."""
    return refresh_token(current_user)
