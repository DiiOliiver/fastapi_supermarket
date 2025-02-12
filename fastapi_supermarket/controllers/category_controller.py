from http import HTTPStatus

from fastapi import APIRouter

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.schemas.category_schema import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
)
from fastapi_supermarket.services.category_service import (
    create,
    delete,
    find_all,
    find_by_id,
    update,
)

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=CategoryResponse
)
def create_category(
    category: CategoryCreate, session: T_Session, current_user: T_CurrentUser
) -> CategoryResponse:
    """Cria uma nova categoria."""
    return create(category, session)


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=CategoryListResponse
)
def read_categories(
    session: T_Session,
    current_user: T_CurrentUser,
    skip: int = 0,
    limit: int = 10,
) -> CategoryListResponse:
    """Retorna todas os categorias cadastrados."""
    return find_all(session, skip, limit)


@router.get(
    '/{category_id}',
    status_code=HTTPStatus.OK,
    response_model=CategoryResponse,
)
def get_category(
    category_id: int, session: T_Session, current_user: T_CurrentUser
) -> CategoryResponse:
    """Retorna uma categoria por ID."""
    return find_by_id(category_id, session)


@router.put(
    '/{category_id}',
    status_code=HTTPStatus.OK,
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: T_Session,
    current_user: T_CurrentUser,
) -> CategoryResponse:
    """Retorna uma categoria por ID e altera seus registros."""
    return update(category_id, category, session)


@router.delete('/{category_id}', status_code=HTTPStatus.OK)
def delete_category(
    category_id: int, session: T_Session, current_user: T_CurrentUser
) -> dict[str, str]:
    """Retorna uma categoria por ID e remove o registro de consultas."""
    return delete(category_id, session)
