import pytest
from flask.testing import FlaskClient
from ej2b4 import create_app, TEMPLATE
#from jinja2 import Template
from jinja2 import Template,meta,Environment

@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

#def test_template_contains_placeholder():
#    """
#    Verifica que la plantilla importada contiene el marcador de posición {{ nombre }}.
#    """
#    template = Template(TEMPLATE)
#    assert "nombre" in template.module.__dict__, "La plantilla debe contener el marcador de posición {{ nombre }}."


def test_template_contains_placeholder():
    """
    Verifica que la plantilla importada contiene el marcador de posición {{ nombre }}.
    """
    template = Template(TEMPLATE)
    env = Environment()
    parsed_content = env.parse(TEMPLATE)
    undeclared_vars = meta.find_undeclared_variables(parsed_content)

    assert "nombre" in undeclared_vars, "La plantilla debe contener el marcador de posición {{ nombre }}."


def test_greet_endpoint(client):
    """
    Prueba el endpoint /greet/<nombre> para validar que devuelve una página web con un saludo personalizado.
    """
    nombre = "Juan"
    response = client.get(f"/greet/{nombre}")
    assert response.status_code == 200, "El código de estado debe ser 200."
    html_content = response.data.decode("utf-8")
    assert "<!doctype html>" in html_content.lower(), "La respuesta debe contener la declaración <!doctype html>."
    assert "<html>" in html_content.lower(), "La respuesta debe contener la etiqueta <html>."
    assert "<body>" in html_content.lower(), "La respuesta debe contener la etiqueta <body>."
    assert f"¡hola, {nombre.lower()}" in html_content.lower(), "La respuesta debe contener el mensaje '¡Hola, <nombre>!' dentro del cuerpo."
