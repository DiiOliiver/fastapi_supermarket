from http import HTTPStatus

from fastapi_supermarket.schemas.user_schema import UserResponse


def test_create_user_success(client):
    response = client.post(
        '/users',
        json={
            'name': 'Diego',
            'cpf': '00000000000',
            'email': 'diego.oliveira2@teste.com',
            'password': 'Secret123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    user = response.json()
    assert user['name'] == 'Diego'
    assert user['cpf'] == '00000000000'
    assert user['email'] == 'diego.oliveira2@teste.com'


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserResponse.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    assert user['name'] == 'Diego'
    assert user['cpf'] == '00000000000'
    assert user['email'] == 'diego.oliveira2@teste.com'


def test_update_user_success(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'name': 'Maria Oliveira',
            'cpf': '00000000001',
            'email': 'maria.oliveira@teste.com',
            'password': 'Secret123',
        },
    )
    assert response.status_code == HTTPStatus.OK
    user = response.json()
    assert user['name'] == 'Maria Oliveira'
    assert user['cpf'] == '00000000001'
    assert user['email'] == 'maria.oliveira@teste.com'


def test_delete_user_success(client, user):
    response = client.delete(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}
