import pytest
from flask.testing import FlaskClient
from ej2e3 import create_app
import io
import os


@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_post_text(client):
    response = client.post("/text", data="Este es un texto de prueba", content_type="text/plain")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Este es un texto de prueba"
    assert response.content_type == "text/plain"

def test_post_html(client):
    response = client.post("/html", data="<h1>Prueba HTML</h1>", content_type="text/html")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "<h1>Prueba HTML</h1>"
    assert response.content_type == "text/html"

def test_post_json(client):
    response = client.post("/json", json={"key": "value"})
    assert response.status_code == 200
    assert response.json == {"key": "value"}
    assert response.content_type == "application/json"

def test_post_xml(client):
    xml_data = "<root><key>value</key></root>"
    response = client.post("/xml", data=xml_data, content_type="application/xml")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == xml_data
    assert response.content_type == "application/xml"

def test_post_image(client):
    """
    Test POST /image endpoint - should accept an image file and save it
    """
    # Create a test image using scipy.misc.face()
    #from scipy import misc
    from scipy import datasets
    import numpy as np
    from PIL import Image

    # Get the face image from scipy
    #face = misc.face()
    face = datasets.face()

    # Convert to bytes in PNG format
    img = Image.fromarray(face)
    img_bytes_io = io.BytesIO()
    img.save(img_bytes_io, format='PNG')
    img_bytes = img_bytes_io.getvalue()

    # Send the image
    response = client.post(
        "/image",
        data=img_bytes,
        content_type="image/png"
    )

    # Check response
    assert response.status_code == 200
    assert response.is_json
    assert "mensaje" in response.json
    assert "archivo" in response.json

def test_post_binary(client):
    # Create some binary data
    binary_data = os.urandom(64)  # 64 random bytes

    # Send the binary data
    response = client.post(
        "/binary",
        data=binary_data,
        content_type="application/octet-stream"
    )

    # Check response
    assert response.status_code == 200
    assert response.is_json
    assert "mensaje" in response.json
    assert "tamaño" in response.json
    assert response.json["tamaño"] == 64  # Should match the size of our test data
