import json
from datetime import datetime

import pytest

import project.api.users


class AttrDict(dict):
    """Dict-like class that allows access to keys via attribute (dot) syntax."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def test_add_user(test_app, monkeypatch, create_payload):
    def mock_get_user_by_email(email):
        return None

    def mock_add_user(username, email):
        return True

    monkeypatch.setattr(project.api.users, 'get_user_by_email', mock_get_user_by_email)
    monkeypatch.setattr(project.api.users, 'add_user', mock_add_user)

    client = test_app.test_client()
    username = 'joe'
    email = 'joe@example.com'
    payload = create_payload(username, email)
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert email in data['message']


def test_add_user_invalid_json(test_app, monkeypatch, create_payload):
    client = test_app.test_client()
    payload = create_payload()
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'validation failed' in data['message']


def test_add_user_missing_username_key(test_app, monkeypatch, create_payload):
    client = test_app.test_client()
    payload = create_payload(username='joe')
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'validation failed' in data['message']


def test_add_user_missing_email_key(test_app, monkeypatch, create_payload):
    client = test_app.test_client()
    payload = create_payload(email='joe@example.com')
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'validation failed' in data['message']


def test_add_user_duplicated_email(test_app, monkeypatch, create_payload):
    def mock_get_user_by_email(email):
        return True

    def mock_add_user(username, email):
        return True

    monkeypatch.setattr(project.api.users, 'get_user_by_email', mock_get_user_by_email)
    monkeypatch.setattr(project.api.users, 'add_user', mock_add_user)

    client = test_app.test_client()
    payload = create_payload(username='joe', email='joe@example.com')
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'already exists' in data['message']


def test_get_user(test_app, monkeypatch, create_payload):
    # username = 'joe'
    # email = 'joe@example.com'
    #
    # user = add_user(username, email)

    user_id = 1
    username = 'joe'
    email = 'joe@example.com'

    def mock_get_user_by_id(user_id):
        return {
            'id': user_id,
            'username': username,
            'email': email,
            'created_date': datetime.now(),
        }

    monkeypatch.setattr(project.api.users, 'get_user_by_id', mock_get_user_by_id)

    client = test_app.test_client()
    response = client.get(f'/users/{user_id}')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert username in data['username']
    assert email in data['email']


def test_get_user_with_wrong_id(test_app, monkeypatch, create_payload):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.api.users, 'get_user_by_id', mock_get_user_by_id)

    client = test_app.test_client()
    response = client.get('/users/1000')
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert 'does not exists' in data['message']


def test_get_all_users(test_app, monkeypatch, create_payload):
    user_data = [
        {'id': 1, 'username': 'joe', 'email': 'joe@example.com'},
        {'id': 2, 'username': 'jane', 'email': 'jane@example.com'},
    ]

    def mock_get_all_users():
        return user_data

    monkeypatch.setattr(project.api.users, 'get_all_users', mock_get_all_users)

    client = test_app.test_client()
    response = client.get('/users')
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert len(data) == len(user_data)
    for index, user_entry in enumerate(user_data):
        assert user_entry['username'] in data[index]['username']
        assert user_entry['email'] in data[index]['email']


def test_delete_user(test_app, monkeypatch, create_payload):
    user_id = 1
    username = 'joe'
    email = 'joe@example.com'

    def mock_get_user_by_id(user_id):
        user = AttrDict()
        user.update({'id': user_id, 'username': username, 'email': email})
        return user

    def mock_delete_user(user):
        return True

    monkeypatch.setattr(project.api.users, 'get_user_by_id', mock_get_user_by_id)
    monkeypatch.setattr(project.api.users, 'delete_user', mock_delete_user)

    client = test_app.test_client()
    response = client.delete(f'/users/{user_id}')
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert email in data['message']
    assert 'was deleted' in data['message']


def test_delete_user_with_wrong_id(test_app, monkeypatch, create_payload):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.api.users, 'get_user_by_id', mock_get_user_by_id)

    user_id = 1000
    client = test_app.test_client()
    response = client.delete(f'/users/{user_id}')
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert 'does not exists' in data['message']
    assert str(user_id) in data['message']


def test_update_user(test_app, monkeypatch, create_payload):
    user_id = 1
    username = 'joe'
    email = 'joe@example.com'

    def mock_get_user_by_id(user_id):
        user = AttrDict()
        user.update({'id': user_id, 'username': username, 'email': email})
        return user

    def mock_update_user(user, username, email):
        return True

    monkeypatch.setattr(project.api.users, 'get_user_by_id', mock_get_user_by_id)
    monkeypatch.setattr(project.api.users, 'update_user', mock_update_user)

    payload = create_payload(username, email)
    client = test_app.test_client()
    response = client.put(f'/users/{user_id}', **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert email in data['message']


@pytest.mark.parametrize(
    'user_id, user_data, status_code, message',
    [
        [1, {}, 400, 'validation failed'],
        [1, {'email': 'joe@example.com'}, 400, 'validation failed'],
        [1000, {'username': 'joe', 'email': 'joe@example.com'}, 404, 'does not exists'],
    ],
)
def test_update_user_with_invalid_payload(
    test_app, monkeypatch, create_payload, user_id, user_data, status_code, message
):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.api.users, 'get_user_by_id', mock_get_user_by_id)

    payload = create_payload(**user_data)
    client = test_app.test_client()
    response = client.put(f'/users/{user_id}', **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == status_code
    assert message in data['message']
