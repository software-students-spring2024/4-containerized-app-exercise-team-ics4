import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data

def test_update_status(client):
    data = {
        "loading": True,
        "sound1": "test_sound1",
        "confidence1": "test_confidence1",
        "sound2": "test_sound2", 
        "confidence2": "test_confidence2",
        "sound3": "test_sound3",
        "confidence3": "test_confidence3",
        "microphoneConnected": True
    }
    response = client.post('/update', json=data)
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == "Status updated successfully"

    # Check if status is updated correctly
    updated_response = client.get('/')
    assert updated_response.status_code == 200
    assert b'test_sound1' in updated_response.data
    assert b'test_confidence1' in updated_response.data
    assert b'test_sound2' in updated_response.data
    assert b'test_confidence2' in updated_response.data
    assert b'test_sound3' in updated_response.data
    assert b'test_confidence3' in updated_response.data
    assert b'microphoneConnected: true' in updated_response.data

def test_no_changes_made(client):
    data = {
        "loading": False,
        "sound1": "",
        "confidence1": "",
        "sound2": "", 
        "confidence2": "",
        "sound3": "",
        "confidence3": "",
        "microphoneConnected": False
    }
    response = client.post('/update', json=data)
    assert response.status_code == 200
    assert response.json['success'] == False
    assert response.json['message'] == "No changes made"