import json

import pytest

from project import bcrypt, db  # noqa
from project.api.users.crud import get_user_by_id
from project.api.users.models import User  # noqa


def test_add_user(test_app, test_database, create_payload):
    client = test_app.test_client()
    username = "joe"
    email = "joe@example.com"
    payload = create_payload(username=username, email=email, password="123")
    response = client.post("/users", **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert email in data["message"]
    assert "password" not in data


def test_add_user_invalid_json(test_app, test_database, create_payload):
    client = test_app.test_client()
    payload = create_payload()
    response = client.post("/users", **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "validation failed" in data["message"]


def test_add_user_missing_username_key(test_app, test_database, create_payload):
    client = test_app.test_client()
    payload = create_payload(username="joe")
    response = client.post("/users", **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "validation failed" in data["message"]


def test_add_user_missing_email_key(test_app, test_database, create_payload):
    client = test_app.test_client()
    payload = create_payload(email="joe@example.com")
    response = client.post("/users", **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "validation failed" in data["message"]


def test_add_user_duplicated_email(test_app, test_database, create_payload):
    client = test_app.test_client()
    payload = create_payload(username="joe", email="joe@example.com", password="123")
    client.post("/users", **payload)
    response = client.post("/users", **payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "already exists" in data["message"]


def test_get_user(test_app, test_database, add_user, create_payload):
    username = "joe"
    email = "joe@example.com"

    user = add_user(username, email)

    client = test_app.test_client()
    response = client.get(f"/users/{user.id}")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert username in data["username"]
    assert email in data["email"]
    assert "password" not in data


def test_get_user_with_wrong_id(test_app, test_database, create_payload):
    client = test_app.test_client()
    response = client.get("/users/1000")
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert "does not exists" in data["message"]


def test_get_all_users(test_app, test_database, add_user, create_payload):
    user_data = [
        {"username": "joe", "email": "joe@example.com"},
        {"username": "jane", "email": "jane@example.com"},
    ]
    users = []
    users.append(add_user(user_data[0]["username"], user_data[0]["email"]))
    users.append(add_user(user_data[1]["username"], user_data[1]["email"]))

    client = test_app.test_client()
    response = client.get("/users")
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert len(data) == len(user_data)
    for index, user_entry in enumerate(user_data):
        assert user_entry["username"] in data[index]["username"]
        assert user_entry["email"] in data[index]["email"]
        assert "password" not in data[index]


def test_delete_user(test_app, test_database, add_user, create_payload):
    username = "joe"
    email = "joe@example.com"

    user = add_user(username, email)

    user_id = user.id

    client = test_app.test_client()
    response1 = client.delete(f"/users/{user_id}")
    data1 = json.loads(response1.data.decode())

    assert response1.status_code == 200
    assert email in data1["message"]
    assert "was deleted" in data1["message"]

    response2 = client.get(f"/users/{user_id}")
    data2 = json.loads(response2.data.decode())

    assert response2.status_code == 404
    assert "does not exists" in data2["message"]


def test_delete_user_with_wrong_id(test_app, test_database, create_payload):
    user_id = 1000
    client = test_app.test_client()
    response = client.delete(f"/users/{user_id}")
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert "does not exists" in data["message"]
    assert str(user_id) in data["message"]


def test_update_user(test_app, test_database, add_user, create_payload):
    username = "joe"
    email = "joe@example.com"

    user = add_user(username, email)

    test_database.session.add(user)
    test_database.session.commit()

    payload = create_payload(username=username, email=email)
    client = test_app.test_client()
    response = client.put(f"/users/{user.id}", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert email in data["message"]
    assert "password" not in data


def test_update_user_with_password(test_app, test_database, add_user, create_payload):
    username = "joe"
    email = "joe@example.com"
    password1 = "A"
    password2 = "B"

    user = add_user(username, email, password1)
    assert bcrypt.check_password_hash(user.password, password1)

    payload = create_payload(username=username, email=email, password=password2)
    client = test_app.test_client()
    response = client.put(f"/users/{user.id}", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert email in data["message"]
    assert "password" not in data

    user = get_user_by_id(user.id)
    assert bcrypt.check_password_hash(user.password, password1)
    assert not bcrypt.check_password_hash(user.password, password2)


@pytest.mark.parametrize(
    "user_id, user_data, status_code, message",
    [
        [1, {}, 400, "validation failed"],
        [1, {"email": "joe@example.com"}, 400, "validation failed"],
        [1000, {"username": "joe", "email": "joe@example.com"}, 404, "does not exists"],
    ],
)
def test_update_user_with_invalid_payload(
    test_app, test_database, create_payload, user_id, user_data, status_code, message
):

    payload = create_payload(**user_data)
    client = test_app.test_client()
    response = client.put(f"/users/{user_id}", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == status_code
    assert message in data["message"]
