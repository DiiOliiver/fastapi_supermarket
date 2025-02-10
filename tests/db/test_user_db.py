from sqlalchemy import select

from fastapi_supermarket.models import User


def test_create_user(session):
    user = User(
        name='Diego Feitosa',
        email='diego2.feitosa@teste.com',
        cpf='12345678901',
        password='Admin@123',
    )
    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).filter_by(email='diego2.feitosa@teste.com')
    )

    assert result.name == 'Diego Feitosa'
    assert result.email == 'diego2.feitosa@teste.com'
    assert result.cpf == '12345678901'
