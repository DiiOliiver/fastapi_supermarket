from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi_supermarket.core.database import get_session
from fastapi_supermarket.models import User
from fastapi_supermarket.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)

router = APIRouter()


@router.post(
    '/users', status_code=HTTPStatus.CREATED, response_model=UserResponse
)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.cpf == user.cpf) | (User.email == user.email))
    )

    if db_user:
        if db_user.cpf == user.cpf:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Cpf already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        name=user.name,
        cpf=user.cpf,
        email=user.email,
        password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get(
    '/users', status_code=HTTPStatus.OK, response_model=UserListResponse
)
def read_users(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(skip)).all()
    return {'users': users}


@router.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponse
)
def get_user(user_id: int):
    if user_id > len([1, 2, 3, 4, 5]) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    # service.findById
    return {
        'id': user_id,
        'name': 'Diego',
        'cpf': '00000000000',
        'email': 'diego.oliveira2@teste.com',
    }


@router.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponse
)
def update_user(
    user_id: int, user: UserUpdate, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    db_user.email = user.email
    db_user.name = user.name
    db_user.cpf = user.cpf
    db_user.password = user.password
    db_user.updated_at = func.now()

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/users/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    db_user.deleted_at = func.now()

    session.add(db_user)
    session.commit()

    return {'message': 'User deleted!'}
