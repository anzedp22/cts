from fastapi.testclient import TestClient

from .main import CTS

client = TestClient(CTS)


# Function to read version from version.txt
def read_version():
    with open("version.txt", "r") as file:
        version = file.read().strip()
    return version


# Test helloo world path
def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# Test ping path
def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200


# Test version path
def test_version():
    expected_version = read_version()
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": expected_version}
