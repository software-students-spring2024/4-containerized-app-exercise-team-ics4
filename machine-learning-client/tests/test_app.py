def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type

def test_update_status(client):
    test_data = {
        "loading": False,
        "sound1": "Speech",
        "confidence1": 0.02,
        "sound2": "Knock",
        "confidence2": 0.23,
        "sound3": "Clap",
        "confidence3": 0.49,
        "microphoneConnected": True
    }
    response = client.post('/update', json=test_data)
    data = response.get_json()

    assert response.status_code == 200
    assert data['success'] == True
    assert data['message'] == "Status updated successfully"