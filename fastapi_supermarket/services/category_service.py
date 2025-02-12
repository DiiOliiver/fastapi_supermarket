from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select

from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.models import Category
from fastapi_supermarket.schemas.category_schema import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
)


def create(category: CategoryCreate, session: T_Session) -> CategoryResponse:
    db_category = Category(description=category.description)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def find_all(
    session: T_Session,
    skip: int,
    limit: int,
) -> CategoryListResponse:
    categories = session.scalars(
        select(Category)
        .where(Category.deleted_at.is_(None))
        .limit(limit)
        .offset(skip)
    ).all()
    return {'categories': categories}


def find_by_id(category_id: int, session: T_Session) -> CategoryResponse:
    query = select(Category).where(
        Category.deleted_at.is_(None) & (Category.id == category_id)
    )
    category = session.scalar(query)
    return category


def update(
    category_id: int, category: CategoryUpdate, session: T_Session
) -> CategoryResponse:
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


def delete(category_id: int, session: T_Session) -> dict[str, str]:
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
