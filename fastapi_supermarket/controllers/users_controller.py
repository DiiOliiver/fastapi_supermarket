from http import HTTPStatus

from fastapi import APIRouter

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from fastapi_supermarket.services.user_service import (
    create,
    delete,
    find_all,
    find_by_id,
    update,
)

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: T_Session) -> UserResponse:
    """Cria uma novo usuário."""
    return create(user, session)


@router.get('/', status_code=HTTPStatus.OK, response_model=UserListResponse)
def read_users(
    session: T_Session,
    current_user: T_CurrentUser,
    skip: int = 0,
    limit: int = 10,
) -> UserListResponse:
    """Retorna todos os usuários cadastrados."""
    return find_all(session, skip, limit)


@router.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponse
)
def get_user(
    user_id: int,
    current_user: T_CurrentUser,
) -> UserResponse:
    """Retorna um usuário por ID."""
    return find_by_id(user_id, current_user)


@router.put(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: T_Session,
    current_user: T_CurrentUser,
) -> UserResponse:
    """Retorna um usuário por ID e altera seus registros."""
    return update(user_id, user, session, current_user)


@router.delete('/{user_id}', status_code=HTTPStatus.OK)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
) -> dict[str, str]:
    """Retorna um usuário por ID e remove o registro de consultas."""
    return delete(user_id, session, current_user)
