from http import HTTPStatus

from freezegun import freeze_time


def test_auth(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_authentication_credentials_is_invalid_password_in_auth(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'secret-invalid'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Authentication credentials is invalid.'
    }


def test_authentication_credentials_is_invalid_email_in_auth(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong@teste.com', 'password': 'secret-invalid'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Authentication credentials is invalid.'
    }


def test_token_expired_after_time(client, user):
    with freeze_time('2025-02-10 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-02-10 12:31:00'):
        response = client.get(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials.'}


def test_refresh_token_after_time(client, token):
    response = client.post(
        '/auth/token/refresh',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2025-02-10 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time('2025-02-10 12:31:00'):
        response = client.post(
            '/auth/token/refresh',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials.'}
