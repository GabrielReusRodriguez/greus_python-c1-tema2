"""
Enunciado:
Desarrolla una aplicación web básica con Flask que responda a una petición GET y devuelva una pequeña página web.
La aplicación debe tener el siguiente endpoint:

1. `GET /greet/<nombre>`: Devuelve una página web que saluda al usuario cuyo nombre se pasa como parámetro en la URL.

Tu tarea es completar la implementación de la función create_app() y del endpoint solicitado.
Además, debes crear una plantilla HTML utilizando Jinja2 que reciba una variable `nombre` y la utilice para mostrar un mensaje de saludo.

Nota: Asegúrate de incluir una estructura HTML válida en la plantilla.
"""

from flask import Flask, render_template_string

# Implementa la plantilla HTML aquí
# Las variables van en doble {{}}
#<!doctype html>

TEMPLATE = """
<!doctype html>
<html>
<head>
 <title>¡Hola, {{ nombre }}!</title>
</head>
<body>
<h1>¡Hola, {{ nombre }}!</h1>
</body>
</html>
"""

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/greet/<nombre>', methods=['GET'])
    def greet(nombre):
        """
        Devuelve una página web que saluda al usuario utilizando una plantilla Jinja2
        """
        # Utiliza render_template_string para renderizar la plantilla con el nombre proporcionado:
        # render_:template_string de flask utiliza jinja2., le tenemos que pasar las variables...
        return render_template_string(source= TEMPLATE, nombre =  nombre)
        #pass

    return app

from jinja2 import Template,meta
from jinja2 import Environment, meta
from jinja2.nodes import Name

if __name__ == '__main__':
    
    template = Template(TEMPLATE)

    env = Environment()
    parsed_content = env.parse(TEMPLATE)
    print("undeclared=", meta.find_undeclared_variables(parsed_content))

    app = create_app()
    app.run(debug=True)
