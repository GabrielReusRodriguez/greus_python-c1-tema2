import pytest
from flask import Flask
from flask.testing import FlaskClient
#from ej2c2 import create_app
from ej2c2 import create_app

@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_tasks_empty(client):
    """Test GET /tasks with an empty task list"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json == []

def test_add_task(client):
    """Test POST /tasks with valid data"""
    response = client.post("/tasks", json={"name": "Comprar leche"})
    assert response.status_code == 201
    assert response.json == {"id": 1, "name": "Comprar leche"}

    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "Comprar leche"}]

def test_delete_task(client):
    """Test DELETE /tasks/<id> for an existing task"""
    # First add a task and get its ID from the response
    add_response = client.post("/tasks", json={"name": "Tarea para eliminar"})
    task_id = add_response.json["id"]  # Get the actual ID assigned by the server

    # Then delete it using the retrieved ID
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json == {"message": "Task deleted"}

def test_delete_nonexistent_task(client):
    """Test DELETE /tasks/<id> for a non-existent task"""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json == {"error": "Task not found"}

def test_update_task(client):
    """Test PUT /tasks/<id> for an existing task"""
    # First add a task and get its ID from the response
    add_response = client.post("/tasks", json={"name": "Tarea original"})
    task_id = add_response.json["id"]  # Get the actual ID assigned by the server

    # Then update it
    response = client.put(f"/tasks/{task_id}", json={"name": "Tarea actualizada"})

    # Check if the update was successful:
    assert response.status_code == 200
    assert response.json == {"id": task_id, "name": "Tarea actualizada"}


def test_update_nonexistent_task(client):
    """Test PUT /tasks/<id> for a non-existent task"""
    response = client.put("/tasks/999", json={"name": "Tarea inexistente"})
    assert response.status_code == 404
    assert response.json == {"error": "Task not found"}
