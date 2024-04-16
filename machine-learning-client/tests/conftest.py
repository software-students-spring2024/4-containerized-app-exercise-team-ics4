import pytest
from unittest.mock import patch
import mongomock
from app import app as flask_app

@pytest.fixture(scope='session', autouse=True)
def mock_db():
    with patch('pymongo.MongoClient', new_callable=lambda: mongomock.MongoClient):
        yield

@pytest.fixture(scope='session')
def app():
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        yield flask_app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()