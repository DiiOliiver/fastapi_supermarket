from http import HTTPStatus

from fastapi_supermarket.schemas.user_schema import UserResponse

request_user_create = {
    'name': 'Diego',
    'cpf': '00000000003',
    'email': 'diego.oliveira3@teste.com',
    'password': 'Secret123',
}

request_user_update = {
    'name': 'Maria Oliveira',
    'cpf': '00000000001',
    'email': 'maria.oliveira@teste.com',
    'password': 'Secret123',
}


def test_create_user(client, token):
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json=request_user_create,
    )
    assert response.status_code == HTTPStatus.CREATED
    user = response.json()
    assert user['name'] == 'Diego'
    assert user['cpf'] == '00000000003'
    assert user['email'] == 'diego.oliveira3@teste.com'


def test_user_already_exists_in_create_user(client, token, user):
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': user.name,
            'cpf': user.cpf,
            'email': user.email,
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User already exists.'}


def test_read_users(client, user, token):
    user_schema = UserResponse.model_validate(user).model_dump()
    response = client.get(
        '/users', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_users_with_users(client, user, token):
    user_schema = UserResponse.model_validate(user).model_dump()
    response = client.get(
        '/users', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client, user, token):
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    assert user['name'] == 'Diego'
    assert user['cpf'] == '00000000000'
    assert user['email'] == 'diego.oliveira2@teste.com'


def test_not_enough_permissions_in_get_user(client, user, token):
    response = client.get(
        '/users/7', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions!'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=request_user_update,
    )
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    assert user['name'] == 'Maria Oliveira'
    assert user['cpf'] == '00000000001'
    assert user['email'] == 'maria.oliveira@teste.com'


def test_not_enough_permissions_in_update_user(client, user, token):
    response = client.put(
        '/users/7',
        headers={'Authorization': f'Bearer {token}'},
        json=request_user_update,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions!'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_not_enough_permissions_in_delete_user(client, user, token):
    response = client.delete(
        '/users/7', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions!'}


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalid'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}
