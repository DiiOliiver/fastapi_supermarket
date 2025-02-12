from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select

from fastapi_supermarket.annotaded.t_currentuser import T_CurrentUser
from fastapi_supermarket.annotaded.t_session import T_Session
from fastapi_supermarket.core.security import (
    get_password_hash,
)
from fastapi_supermarket.models import User
from fastapi_supermarket.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)


def create(user: UserCreate, session: T_Session) -> UserResponse:
    db_user = session.scalar(
        select(User).where(
            User.deleted_at.is_(None)
            & ((User.cpf == user.cpf) | (User.email == user.email))
        )
    )

    if db_user:
        if (db_user.cpf == user.cpf) & (db_user.email == user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User already exists.',
            )

    db_user = User(
        name=user.name,
        cpf=user.cpf,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def find_all(
    session: T_Session,
    skip: int,
    limit: int,
) -> UserListResponse:
    users = session.scalars(
        select(User).where(User.deleted_at.is_(None)).limit(limit).offset(skip)
    ).all()
    return {'users': users}


def find_by_id(user_id: int, current_user: T_CurrentUser) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions!',
        )
    return current_user


def update(
    user_id: int,
    user: UserUpdate,
    session: T_Session,
    current_user: T_CurrentUser,
) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions!',
        )

    current_user.name = user.name
    current_user.email = user.email
    current_user.cpf = user.cpf
    if user.password:
        current_user.password = get_password_hash(user.password)
    current_user.updated_at = func.now()

    session.commit()
    session.refresh(current_user)

    return current_user


def delete(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
) -> dict[str, str]:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions!',
        )

    current_user.deleted_at = func.now()

    session.commit()
    session.refresh(current_user)

    return {'message': 'User deleted!'}
