from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.models import Category
from fastapi_supermarket.schemas.category_schema import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
)

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=CategoryResponse
)
def create_category(
    category: CategoryCreate, session: T_Session, current_user: T_CurrentUser
):
    db_category = Category(description=category.description)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=CategoryListResponse
)
def read_categories(
    session: T_Session,
    current_user: T_CurrentUser,
    skip: int = 0,
    limit: int = 10,
):
    categories = session.scalars(
        select(Category)
        .where(Category.deleted_at.is_(None))
        .limit(limit)
        .offset(skip)
    ).all()
    return {'categories': categories}


@router.get(
    '/{category_id}',
    status_code=HTTPStatus.OK,
    response_model=CategoryResponse,
)
def get_category(
    category_id: int, session: T_Session, current_user: T_CurrentUser
):
    query = select(Category).where(
        Category.deleted_at.is_(None) & (Category.id == category_id)
    )
    category = session.scalar(query)
    return category


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
):
    query = select(Category).where(
        Category.deleted_at.is_(None) & (Category.id == category_id)
    )
    db_category = session.scalar(query)
    if not db_category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Category not found'
        )

    if category.description:
        db_category.description = category.description
        db_category.updated_at = func.now()

    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete('/{category_id}', status_code=HTTPStatus.OK)
def delete_category(
    category_id: int, session: T_Session, current_user: T_CurrentUser
):
    query = select(Category).where(
        Category.deleted_at.is_(None) & (Category.id == category_id)
    )
    db_category = session.scalar(query)
    if not db_category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Category not found'
        )

    db_category.deleted_at = func.now()
    session.commit()
    session.refresh(db_category)

    return {'message': 'Category deleted!'}
