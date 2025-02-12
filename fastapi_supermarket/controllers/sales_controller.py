from fastapi import APIRouter

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.schemas.sales_schema import (
    SalesCreate,
    SalesListResponse,
    SalesResponse,
)
from fastapi_supermarket.services.sales_service import (
    create,
    find_all,
    find_by_id,
)

router = APIRouter(prefix='/sales', tags=['Sales'])


@router.post('/', response_model=SalesResponse)
def create_sale(
    sale: SalesCreate, session: T_Session, current_user: T_CurrentUser
) -> SalesResponse:
    """Cria uma nova venda."""
    return create(sale, session)


@router.get('/', response_model=SalesListResponse)
def get_all_sales(
    session: T_Session, current_user: T_CurrentUser
) -> SalesListResponse:
    """Retorna todas as vendas cadastradas."""
    return find_all(session)


@router.get('/{sale_id}', response_model=SalesResponse)
def get_sale(
    sale_id: int, session: T_Session, current_user: T_CurrentUser
) -> SalesResponse:
    """Retorna uma venda por ID."""
    return find_by_id(sale_id, session)
