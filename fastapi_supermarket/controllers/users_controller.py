from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_supermarket.core.database import get_session
from fastapi_supermarket.core.security import (
    get_current_user,
    get_password_hash,
)
from fastapi_supermarket.models import User
from fastapi_supermarket.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
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


@router.get('/', status_code=HTTPStatus.OK, response_model=UserListResponse)
def read_users(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    users = session.scalars(
        select(User).where(User.deleted_at.is_(None)).limit(limit).offset(skip)
    ).all()
    return {'users': users}


@router.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponse
)
def get_user(
    user_id: int,
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions!',
        )

    return current_user


@router.put(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
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


@router.delete('/{user_id}', status_code=HTTPStatus.OK)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions!',
        )

    current_user.deleted_at = func.now()

    session.commit()
    session.refresh(current_user)

    return {'message': 'User deleted!'}
