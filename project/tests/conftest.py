import pytest

from project import create_app, db


@pytest.fixture(scope='module')
def test_app():
    '''Entry point for app testing'''
    app = create_app()
    app.config.from_object('project.config.TestingConfig')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_database():
    '''Entry point for database testing'''
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
