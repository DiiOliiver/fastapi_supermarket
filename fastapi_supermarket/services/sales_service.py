from fastapi import HTTPException
from sqlalchemy import select

from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.models import ProductSales, Sales
from fastapi_supermarket.schemas.product_schema import ProductPublic
from fastapi_supermarket.schemas.sales_schema import (
    SalesCreate,
    SalesListResponse,
    SalesResponse,
)


def create(sale: SalesCreate, session: T_Session) -> SalesResponse:
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


def find_all(session: T_Session) -> SalesListResponse:
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


def find_by_id(sale_id: int, session: T_Session) -> SalesResponse:
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
