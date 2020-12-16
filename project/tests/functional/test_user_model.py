def test_passwords_are_random(test_app, test_database, add_user):
    user1 = add_user("joe", "joe@example.com", "veryrandompassword")
    user2 = add_user("jane", "jane@example.com", "veryrandompassword")
    assert user1.password != user2.password
