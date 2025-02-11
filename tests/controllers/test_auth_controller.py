from http import HTTPStatus


def test_auth(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_authentication_credentials_is_invalid_in_auth(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'secret-invalid'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Authentication credentials is invalid.'
    }
