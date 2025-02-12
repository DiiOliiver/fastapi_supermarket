from http import HTTPStatus

from fastapi import APIRouter

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.schemas.product_schema import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from fastapi_supermarket.services.product_service import (
    create,
    delete,
    find_all,
    find_by_id,
    update,
)

router = APIRouter(prefix='/products', tags=['Products'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProductResponse
)
def create_product(
    product: ProductCreate, session: T_Session, current_user: T_CurrentUser
) -> ProductResponse:
    """Cria uma novo produto."""
    return create(product, session)


@router.get('/', status_code=HTTPStatus.OK, response_model=ProductListResponse)
def read_products(
    session: T_Session,
    current_user: T_CurrentUser,
    skip: int = 0,
    limit: int = 10,
) -> ProductListResponse:
    """Retorna todos os produtos cadastrados."""
    return find_all(session, skip=skip, limit=limit)


@router.get(
    '/{product_id}',
    status_code=HTTPStatus.OK,
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
) -> ProductResponse:
    """Retorna um produto por ID."""
    return find_by_id(product_id, session)


@router.put(
    '/{product_id}', status_code=HTTPStatus.OK, response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    session: T_Session,
    current_user: T_CurrentUser,
) -> ProductResponse:
    """Retorna um produto por ID e altera seus registros."""
    return update(product_id, product, session)


@router.delete('/{product_id}', status_code=HTTPStatus.OK)
def delete_product(
    product_id: int, session: T_Session, current_user: T_CurrentUser
) -> dict[str, str]:
    """Retorna um produto por ID e remove o registro de consultas."""
    return delete(product_id, session)
