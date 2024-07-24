from fastapi.testclient import TestClient

from .main import CTS

client = TestClient(CTS)


# Test helloo world path
def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# Test ping path
def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
