from jwt import decode

from fastapi_supermarket.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


def test_create_access_token_success():
    data = {'sub': 'teste@test.com'}
    token = create_access_token(data)
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded['sub'] == data['sub']
    assert decoded['exp'] is not None
