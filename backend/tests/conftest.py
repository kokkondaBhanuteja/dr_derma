# tests/conftest.py
import os
import pytest
from app import create_app
from app.db.mysql import db as _db

@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    _app = create_app('testing')
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.fixture(scope='session')
def db(app):
    """Create database for the tests."""
    _db.create_all()
    yield _db
    _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session(
        options={"bind": connection, "binds": {}}
    )
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()