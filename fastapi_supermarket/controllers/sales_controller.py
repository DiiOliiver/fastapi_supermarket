from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.models import ProductSales, Sales
from fastapi_supermarket.schemas.product_schema import ProductPublic
from fastapi_supermarket.schemas.sales_schema import (
    SalesCreate,
    SalesListResponse,
    SalesResponse,
)

router = APIRouter(prefix='/sales', tags=['Sales'])


@router.post('/', response_model=SalesResponse)
def create_sale(
    sale: SalesCreate, session: T_Session, current_user: T_CurrentUser
):
    """Cria uma nova venda e os produtos associados."""
    new_sale = Sales(id_user=sale.id_user)
    session.add(new_sale)
    session.commit()
    session.refresh(new_sale)

    product_sales = [
        ProductSales(id_sale=new_sale.id, id_product=product.id_product)
        for product in sale.products
    ]
    session.add_all(product_sales)
    session.commit()

    return SalesResponse(
        id=new_sale.id,
        id_user=new_sale.id_user,
        products=[
            ProductPublic(
                category=ps.product.category.description,
                description=ps.product.description,
                price=ps.product.price,
            )
            for ps in product_sales
        ],
    )


@router.get('/', response_model=SalesListResponse)
def get_all_sales(session: T_Session, current_user: T_CurrentUser):
    """Retorna todas as vendas cadastradas."""
    query = select(Sales).where(Sales.deleted_at.is_(None))
    sales = session.scalars(query).all()

    return SalesListResponse(
        sales=[
            SalesResponse(
                id=sale.id,
                id_user=sale.id_user,
                products=[
                    ProductPublic(
                        category=ps.product.category.description,
                        description=ps.product.description,
                        price=ps.product.price,
                    )
                    for ps in sale.products
                ],
            )
            for sale in sales
        ],
    )


@router.get('/{sale_id}', response_model=SalesResponse)
def get_sale(sale_id: int, session: T_Session, current_user: T_CurrentUser):
    """Retorna uma venda específica pelo ID."""
    sale = session.get(Sales, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail='Venda não encontrada')
    return SalesResponse(
        id=sale.id,
        id_user=sale.id_user,
        products=[
            ProductPublic(
                category=ps.product.category.description,
                description=ps.product.description,
                price=ps.product.price,
            )
            for ps in sale.products
        ],
    )
