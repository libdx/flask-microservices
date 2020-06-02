import json

from project import db
from project.api.models import User


def create_payload(username=None, email=None):
    data = {}
    if username:
        data['username'] = username
    if email:
        data['email'] = email
    return {
        'data': json.dumps(data),
        'content_type': 'application/json',
    }


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    username = 'joe'
    email = 'joe@example.com'
    payload = create_payload(username, email)
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert email in data['message']


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    payload = create_payload()
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'validation failed' in data['message']


def test_add_user_missing_username_key(test_app, test_database):
    client = test_app.test_client()
    payload = create_payload(username='joe')
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'validation failed' in data['message']


def test_add_user_missing_email_key(test_app, test_database):
    client = test_app.test_client()
    payload = create_payload(email='joe@example.com')
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'validation failed' in data['message']


def test_add_user_duplicated_email(test_app, test_database):
    client = test_app.test_client()
    payload = create_payload(username='joe', email='joe@example.com')
    client.post('/users', **payload)
    response = client.post('/users', **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'already exists' in data['message']


def test_get_user(test_app, test_database, add_user):
    username = 'joe'
    email = 'joe@example.com'

    user = add_user(username, email)

    client = test_app.test_client()
    response = client.get(f'/users/{user.id}')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert username in data['username']
    assert email in data['email']


def test_get_user_with_missing_id(test_app, test_database):
    client = test_app.test_client()
    response = client.get('/users/1000')
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert 'does not exists' in data['message']


def test_get_all_users(test_app, test_database, add_user):
    user_data = [
        {'username': 'joe', 'email': 'joe@example.com'},
        {'username': 'jane', 'email': 'jane@example.com'},
    ]
    users = []
    users.append(add_user(user_data[0]['username'], user_data[0]['email']))
    users.append(add_user(user_data[1]['username'], user_data[1]['email']))

    client = test_app.test_client()
    response = client.get('/users')
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert len(data) == len(user_data)
    for index, user_entry in enumerate(user_data):
        assert user_entry['username'] in data[index]['username']
        assert user_entry['email'] in data[index]['email']
