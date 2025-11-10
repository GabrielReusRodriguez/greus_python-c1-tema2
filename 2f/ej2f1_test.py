import pytest
from flask.testing import FlaskClient
from ej2f1 import create_app

@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_main_home_route(client):
    """
    Prueba la ruta principal '/' del blueprint 'main'
    Debe responder con un mensaje de bienvenida
    """
    response = client.get("/api/v1/")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.data, "La respuesta debe contener datos"
    assert b"Bienvenida".lower() in response.data.lower() or \
           b"Benvinguda".lower() in response.data.lower() or \
           b"Welcome".lower() in response.data.lower(), \
           "La respuesta debe contener un mensaje de bienvenida"

def test_main_about_route(client):
    """
    Prueba la ruta '/about' del blueprint 'main'
    Debe responder con información sobre la aplicación
    """
    response = client.get("/api/v1/about")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.data, "La respuesta debe contener datos"
    assert b"aplicaci" in response.data.lower() or b"app" in response.data.lower(), \
           "La respuesta debe contener información sobre la aplicación"

def test_user_profile_route(client):
    """
    Prueba la ruta '/user/profile/<username>' del blueprint 'user'
    Debe responder con un perfil de usuario personalizado
    """
    username = "testuser"
    response = client.get(f"/api/v1/user/profile/{username}")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.data, "La respuesta debe contener datos"
    assert username.encode() in response.data.lower(), \
           "La respuesta debe contener el nombre de usuario proporcionado"

def test_user_list_route(client):
    """
    Prueba la ruta '/user/list' del blueprint 'user'
    Debe responder con una lista de usuarios
    """
    response = client.get("/api/v1/user/list")
    assert response.status_code == 200, "El código de estado debe ser 200"
    assert response.data, "La respuesta debe contener datos"
    assert b"user" in response.data.lower(), \
           "La respuesta debe contener información sobre usuarios"

def test_url_prefix(client):
    """
    Prueba que el prefijo URL '/api/v1' esté correctamente configurado
    Las rutas sin el prefijo no deben funcionar
    """
    # La ruta sin prefijo no debe funcionar
    response_no_prefix = client.get("/")
    assert response_no_prefix.status_code == 404, "La ruta sin prefijo no debe ser accesible"

    # La ruta con prefijo debe funcionar
    response_with_prefix = client.get("/api/v1/")
    assert response_with_prefix.status_code == 200, "La ruta con prefijo debe ser accesible"

def test_blueprint_structure(client):
    """
    Prueba que todos los endpoints necesarios estén disponibles
    Verifica que se hayan implementado correctamente ambos blueprints
    """
    # Rutas del blueprint 'main'
    assert client.get("/api/v1/").status_code == 200
    assert client.get("/api/v1/about").status_code == 200

    # Rutas del blueprint 'user'
    assert client.get("/api/v1/user/profile/testuser").status_code == 200
    assert client.get("/api/v1/user/list").status_code == 200
