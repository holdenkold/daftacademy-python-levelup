from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


def test_method_get():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_method_post():
    response = client.post("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "POST"}


def test_method_put():
    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}


def test_method_delete():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}