from project.api.users.models import User


def test_passwords_are_random(test_app, test_database, add_user):
    user1 = add_user("joe", "joe@example.com", "veryrandompassword")
    user2 = add_user("jane", "jane@example.com", "veryrandompassword")
    assert user1.password != user2.password


def test_encode_access_token(test_app, test_database, add_user):
    user = add_user("aaa", "aaa@example.com", "xyz")
    token = User.encode_token(user.id, "access")
    assert isinstance(token, bytes)


def test_decode_access_token(test_app, test_database, add_user):
    user = add_user("aaa", "aaa@example.com", "xyz")
    token = User.encode_token(user.id, "access")
    assert isinstance(token, bytes)
    assert User.decode_token(token) == user.id


def test_encode_refresh_token(test_app, test_database, add_user):
    user = add_user("aaa", "aaa@example.com", "xyz")
    token = User.encode_token(user.id, "refresh")
    assert isinstance(token, bytes)


def test_decode_refresh_token(test_app, test_database, add_user):
    user = add_user("aaa", "aaa@example.com", "xyz")
    token = User.encode_token(user.id, "refresh")
    assert isinstance(token, bytes)
    assert User.decode_token(token) == user.id
