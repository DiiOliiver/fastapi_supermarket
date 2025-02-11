from jwt import decode

from fastapi_supermarket.core.security import (
    create_access_token,
    settings,
)


def test_create_access_token_success():
    data = {'sub': 'teste@test.com'}
    token = create_access_token(data)
    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decoded['sub'] == data['sub']
    assert decoded['exp'] is not None
