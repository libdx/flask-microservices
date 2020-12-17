import json

import pytest


def test_register(test_app, test_database, create_payload):
    username = "test"
    email = "test@example.com"

    client = test_app.test_client()
    payload = create_payload(username=username, email=email, password="test12345")
    response = client.post("/auth/register", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert username == data["username"]
    assert email == data["email"]
    assert "password" not in data


def test_register_duplicated_email(test_app, test_database, create_payload, add_user):
    username = "test"
    email = "test@example.com"

    add_user(username, email)

    client = test_app.test_client()
    payload = create_payload(username=username, email=email, password="test12345")
    response = client.post("/auth/register", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "already exists" in data["message"]


@pytest.mark.parametrize(
    "user_data, status_code, message",
    [
        [{}, 400, "validation failed"],
        [{"password": "test12345"}, 400, "validation failed"],
        [{"email": "joe@example.com"}, 400, "validation failed"],
        [{"username": "joe"}, 400, "validation failed"],
        [{"username": "joe", "email": "joe@example.com"}, 400, "validation failed"],
        [{"username": "joe", "password": "test12345"}, 400, "validation failed"],
        [
            {"email": "joe@example.com", "password": "test12345"},
            400,
            "validation failed",
        ],
    ],
)
def test_register_with_invalid_payload(
    test_app, test_database, create_payload, user_data, status_code, message
):

    payload = create_payload(**user_data)
    client = test_app.test_client()
    response = client.post("/auth/register", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == status_code
    assert message in data["message"]


def test_registered_login(test_app, test_database, create_payload, add_user):
    email = "test@example.com"
    password = "test12345"
    add_user("test", email, password)

    client = test_app.test_client()
    payload = create_payload(email=email, password=password)
    response = client.post("/auth/login", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert data["access_token"]
    assert data["refresh_token"]


def test_not_registered_login(test_app, test_database, create_payload):
    email = "test@example.com"
    password = "test12345"

    client = test_app.test_client()
    payload = create_payload(email=email, password=password)
    response = client.post("/auth/login", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert "does not exists" in data["message"]
    assert "email" in data["message"]
    assert "password" in data["message"]
    assert "access_token" not in data
    assert "refresh_token" not in data


def test_not_authorised_login(test_app, test_database, create_payload, add_user):
    email = "test@example.com"
    password = "test12345"

    add_user(username="test", email=email, password=password)

    client = test_app.test_client()
    payload = create_payload(email=email, password=password + "6789")
    response = client.post("/auth/login", **payload)
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert "does not exists" in data["message"]
    assert "email" in data["message"]
    assert "password" in data["message"]
    assert "access_token" not in data
    assert "refresh_token" not in data


def test_valid_refresh(test_app, test_database, create_payload, add_user):
    email = "test@example.com"
    password = "test12345"

    add_user(username="test", email=email, password=password)

    client = test_app.test_client()

    login_response = client.post(
        "/auth/login", **create_payload(email=email, password=password)
    )

    tokens = json.loads(login_response.data.decode())
    refresh_token = tokens["refresh_token"]

    assert refresh_token

    refresh_response = client.post(
        "/auth/refresh", **create_payload(refresh_token=refresh_token)
    )
    data = json.loads(refresh_response.data.decode())

    assert refresh_response.status_code == 200
    assert data["access_token"]
    assert data["refresh_token"]


def test_invalid_refresh(test_app, test_database, create_payload):
    client = test_app.test_client()

    response = client.post(
        "/auth/refresh", **create_payload(refresh_token="invalid-token")
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert "invalid token" in data["message"].lower()


def test_invalid_refresh_expired_token(
    test_app, test_database, create_payload, add_user
):

    test_app.config["REFRESH_TOKEN_EXPIRATION"] = -1

    email = "test@example.com"
    password = "test12345"

    add_user(username="test", email=email, password=password)

    client = test_app.test_client()

    login_response = client.post(
        "/auth/login", **create_payload(email=email, password=password)
    )

    tokens = json.loads(login_response.data.decode())
    refresh_token = tokens["refresh_token"]

    assert refresh_token

    refresh_response = client.post(
        "/auth/refresh", **create_payload(refresh_token=refresh_token)
    )
    data = json.loads(refresh_response.data.decode())

    assert refresh_response.status_code == 401
    assert "token expired" in data["message"].lower()


def test_user_status(test_app, test_database, create_payload, add_user):
    username = "test"
    email = "test"
    password = "test123"

    add_user(username=username, email=email, password=password)
    client = test_app.test_client()

    login_response = client.post(
        "/auth/login", **create_payload(email=email, password=password)
    )
    login_data = json.loads(login_response.data.decode())
    access_token = login_data["access_token"]

    status_response = client.get(
        "/auth/status", **create_payload(auth_token=access_token)
    )
    status_data = json.loads(status_response.data.decode())

    assert status_response.status_code == 200
    assert username == status_data["username"]
    assert email == status_data["email"]
    assert "password" not in status_data


def test_user_status_with_invalid_token(test_app, test_database, create_payload):
    client = test_app.test_client()
    response = client.get("/auth/status", **create_payload(auth_token="invalid-token"))
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert "invalid token" in data["message"].lower()
