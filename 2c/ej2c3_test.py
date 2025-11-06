import pytest
from flask.testing import FlaskClient
from ej2c3 import create_app

@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_all_products(client):
    """
    Prueba obtener todos los productos sin filtros
    """
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 8  # Verifica que se devuelvan todos los productos

def test_filter_by_category(client):
    """
    Prueba filtrar productos por categoría
    """
    # Filtrar por categoría "electronics"
    response = client.get("/products?category=electronics")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 5  # Debería haber 4 productos electrónicos
    for product in data:
        assert product["category"] == "electronics"

    # Filtrar por categoría "furniture"
    response = client.get("/products?category=furniture")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2  # Debería haber 2 productos de mobiliario
    for product in data:
        assert product["category"] == "furniture"

def test_filter_by_price_range(client):
    """
    Prueba filtrar productos por rango de precios
    """
    # Filtrar productos con precio >= 500
    response = client.get("/products?min_price=500")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2  # Debería haber 2 productos con precio >= 500
    for product in data:
        assert product["price"] >= 500

    # Filtrar productos con precio <= 200
    response = client.get("/products?max_price=200")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 4  # Debería haber 4 productos con precio <= 200
    for product in data:
        assert product["price"] <= 200

    # Filtrar productos con precio entre 200 y 700
    response = client.get("/products?min_price=200&max_price=700")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 3  # Debería haber 3 productos en ese rango
    for product in data:
        assert product["price"] >= 200 and product["price"] <= 700

def test_filter_by_name(client):
    """
    Prueba filtrar productos por nombre (búsqueda parcial)
    """
    # Filtrar productos que contengan "Pro" en el nombre
    response = client.get("/products?name=Pro")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2  # Debería haber 2 productos con "Pro" en el nombre
    for product in data:
        assert "Pro" in product["name"]

def test_combined_filters(client):
    """
    Prueba combinar varios filtros
    """
    # Filtrar productos electrónicos con precio >= 500
    response = client.get("/products?category=electronics&min_price=500")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2  # Debería haber 2 productos que cumplan ambos criterios
    for product in data:
        assert product["category"] == "electronics"
        assert product["price"] >= 500

    # Filtrar productos con "Pro" en el nombre y precio <= 100
    response = client.get("/products?name=Pro&max_price=100")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1  # Debería haber 1 producto que cumpla ambos criterios
    assert data[0]["name"] == "Coffee Maker Pro"
    assert data[0]["price"] <= 100

def test_filter_no_results(client):
    """
    Prueba filtrar con criterios que no devuelven resultados
    """
    # Filtrar con una categoría que no existe
    response = client.get("/products?category=nonexistent")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 0  # No debería haber productos

    # Filtrar con un rango de precios imposible
    response = client.get("/products?min_price=2000")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 0  # No debería haber productos
