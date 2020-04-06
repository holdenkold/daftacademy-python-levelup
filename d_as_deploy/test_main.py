from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app
import pytest
from fastapi.responses import Response

client = TestClient(app)
client.id = -1
client.patients = dict()


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World during the coronavirus pandemic!"}


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


@pytest.mark.parametrize("recieved", [{"name": "Tom", "surname": "Hanks"}, {"name": "Charles", "surname": "Windsor"}, {"name": "Boris", "surname": "Johnson"}])
def test_patient_post(recieved):
    response = client.post("/patient", json=recieved)
    assert response.status_code == 200
    client.id += 1
    client.patients[client.id] = recieved
    assert response.json() == {"id": client.id, "patient": recieved}


@pytest.mark.parametrize("pk", ['0', '1', '2'])
def test_patient_get(pk: int):
    if pk not in client.patients:
        assert Response(status_code = 204) == client.get("/patient/{0}".format(pk))
    else:
        response = client.get("/patient/{0}".format(pk))
        assert response.status_code == 200
        assert response.text == client.patients[pk]

    