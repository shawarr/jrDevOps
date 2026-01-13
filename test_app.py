import pytest
from app import app
import json

@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to the application!"

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_info(client):
    response = client.get('/info')
    response_json = response.get_json()
    assert response_json["version"] == "1.0.0"
    assert response_json["hostname"] is not None
    assert response_json["hostname"] != ""
    assert response_json["env"] is not None
    assert response_json["env"] != ""
