import pytest

from project import create_app, db
from project.api.models import User


@pytest.fixture(scope='module')
def test_app():
    '''Entry point for app testing'''
    app = create_app()
    app.config.from_object('project.config.TestingConfig')
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def test_database():
    '''Entry point for database testing'''
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def add_user():
    '''Factory to create function that adds new user to database'''

    def _add_user(username, email):
        user = User(username, email)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user
