from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select

from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.models import (
    Category,
    Product,
    ProductSales,
    Sales,
    User,
)
from fastapi_supermarket.schemas.category_schema import CategoryResponse
from fastapi_supermarket.schemas.product_schema import ProductPublic
from fastapi_supermarket.schemas.sales_schema import (
    SalesCreate,
    SalesListResponse,
    SalesResponse,
)
from fastapi_supermarket.schemas.user_schema import UserResponse


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
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Venda não encontrada'
        )
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


def get_sales_summary(
    start_date: str, end_date: str, session: T_Session
) -> dict:
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    total_sales = session.execute(
        select(func.sum(ProductSales.quantity * Product.price))
        .join(ProductSales, Product.id == ProductSales.id_product)
        .join(Sales, Sales.id == ProductSales.id_sale)
        .where(Sales.created_at.between(start_date, end_date))
    ).scalar()
    return {'total_sales': total_sales}


def get_top_product(
    start_date: str, end_date: str, session: T_Session
) -> ProductPublic:
    top_product = session.execute(
        select(
            Product.description,
            Product.price,
            func.sum(ProductSales.quantity).label('total_sold'),
        )
        .join(ProductSales, Product.id == ProductSales.id_product)
        .join(Sales, Sales.id == ProductSales.id_sale)
        .where(Sales.created_at.between(start_date, end_date))
        .group_by(Product.id)
        .order_by(func.sum(ProductSales.quantity).desc())
        .limit(1)
    ).fetchone()

    if not top_product:
        raise HTTPException(
            status_code=404, detail='No product found in the given period'
        )

    return ProductPublic(
        category=top_product[0],
        description=top_product[1],
        price=top_product[2],
    )


def get_top_customer(
    start_date: str, end_date: str, session: T_Session
) -> UserResponse:
    top_customer = session.execute(
        select(User.name, func.count(Sales.id).label('total_purchases'))
        .join(Sales, Sales.id_user == User.id)
        .where(Sales.created_at.between(start_date, end_date))
        .group_by(User.id)
        .order_by(func.count(Sales.id).desc())
        .limit(1)
    ).fetchone()

    if not top_customer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No customer found in the given period',
        )

    return UserResponse(
        id=top_customer[0],
        name=top_customer[1],
        cpf=top_customer[2],
        email=top_customer[3],
    )


def get_revenue_by_category(
    start_date: str, end_date: str, session: T_Session
) -> list[CategoryResponse]:
    revenue_by_category = session.execute(
        select(
            Category.description,
            func.sum(ProductSales.quantity * Product.price).label(
                'total_revenue'
            ),
        )
        .join(Product, Product.id_category == Category.id)
        .join(ProductSales, ProductSales.id_product == Product.id)
        .join(Sales, Sales.id == ProductSales.id_sale)
        .where(Sales.created_at.between(start_date, end_date))
        .group_by(Category.id)
        .order_by(func.sum(ProductSales.quantity * Product.price).desc())
    ).fetchall()

    if not revenue_by_category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No revenue data found for the given period',
        )

    return [
        {'category': category, 'total_revenue': revenue}
        for category, revenue in revenue_by_category
    ]


def get_monthly_average(session: T_Session) -> list[dict]:
    monthly_avg = session.execute(
        select(
            func.date_trunc('month', Sales.created_at).label('month'),
            func.avg(Sales.total_amount).label('avg_sales'),
        )
        .group_by(func.date_trunc('month', Sales.created_at))
        .order_by(func.date_trunc('month', Sales.created_at))
    ).fetchall()

    if not monthly_avg:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='No sales data found'
        )

    return [
        {'month': month, 'avg_sales': avg_sales}
        for month, avg_sales in monthly_avg
    ]
