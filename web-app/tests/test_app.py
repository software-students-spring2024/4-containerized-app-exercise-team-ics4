import pytest
from pymongo import MongoClient
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_status_collection(monkeypatch):
    mock_collection = [
        {"loading": True, "sound1": "test1", "confidence1": 0.5,
         "sound2": "test2", "confidence2": 0.6, "sound3": "test3",
         "confidence3": 0.7, "microphoneConnected": True}
    ]
    def mock_find_one(_):
        return mock_collection[0]

    monkeypatch.setattr('app.status_collection', type('MockCollection', (), {'find_one': mock_find_one}))

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_get_status(client, mock_status_collection):
    response = client.get('/status')
    data = response.get_json()
    assert response.status_code == 200
    assert data['loading'] == True
    assert data['sound1'] == 'test1'
    assert data['confidence1'] == 0.5
    assert data['sound2'] == 'test2'
    assert data['confidence2'] == 0.6
    assert data['sound3'] == 'test3'
    assert data['confidence3'] == 0.7
    assert data['microphoneConnected'] == True

def test_reset_status(client, mock_status_collection):
    response = client.post('/reset_status')
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] == True
    assert data['message'] == 'Status reset to initial state'