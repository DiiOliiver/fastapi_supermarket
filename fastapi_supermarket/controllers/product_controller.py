from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.models import Category, Product
from fastapi_supermarket.schemas.product_schema import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)

router = APIRouter(prefix='/products', tags=['Products'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProductResponse
)
def create_product(
    product: ProductCreate, session: T_Session, current_user: T_CurrentUser
):
    if not session.get(Category, product.id_category):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid category ID'
        )

    db_product = Product(
        id_category=product.id_category,
        description=product.description,
        price=product.price,
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return ProductResponse(
        id=db_product.id,
        description=db_product.description,
        price=db_product.price,
        category=db_product.category.description,
    )


@router.get('/', status_code=HTTPStatus.OK, response_model=ProductListResponse)
def read_products(
    session: T_Session,
    current_user: T_CurrentUser,
    skip: int = 0,
    limit: int = 10,
):
    query = (
        select(Product)
        .where(Product.deleted_at.is_(None))
        .options(joinedload(Product.category))
    )
    products = session.scalars(query.limit(limit).offset(skip)).all()

    if not products:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    return ProductListResponse(
        products=[
            {
                'id': ps.id,
                'description': ps.description,
                'category': ps.category.description,
                'price': ps.price,
            }
            for ps in products
        ],
    )


@router.get(
    '/{product_id}',
    status_code=HTTPStatus.OK,
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    query = (
        select(Product)
        .where(Product.deleted_at.is_(None), Product.id == product_id)
        .options(joinedload(Product.category))
    )
    product = session.scalar(query)

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    return ProductResponse(
        id=product.id,
        description=product.description,
        category=product.category.description,
        price=product.price,
    )


@router.put(
    '/{product_id}', status_code=HTTPStatus.OK, response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    session: T_Session,
    current_user: T_CurrentUser,
):
    query = select(Product).where(
        Product.deleted_at.is_(None) & (Product.id == product_id)
    )
    db_product = session.scalar(query)
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    if product.id_category and not session.get(Category, product.id_category):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid category ID'
        )

    if product.id_category:
        db_product.id_category = product.id_category
    if product.description:
        db_product.description = product.description
    if product.price:
        db_product.price = product.price
    db_product.updated_at = func.now()

    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete('/{product_id}', status_code=HTTPStatus.OK)
def delete_product(
    product_id: int, session: T_Session, current_user: T_CurrentUser
):
    query = select(Product).where(
        Product.deleted_at.is_(None) & (Product.id == product_id)
    )
    db_product = session.scalar(query)
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    db_product.deleted_at = func.now()
    session.commit()
    session.refresh(db_product)

    return {'message': 'Product deleted!'}
