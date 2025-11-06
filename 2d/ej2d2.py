"""
Enunciado:
Desarrolla una aplicación web con Flask que utilice la función abort() para devolver
diferentes códigos de estado HTTP según ciertas condiciones.

La función abort() de Flask permite terminar prematuramente una solicitud con un código
de estado HTTP específico. Esto es útil para indicar errores como recurso no encontrado (404),
acceso prohibido (403), etc.

Tu tarea es implementar los siguientes endpoints:

1. `GET /resource/<id>`: Debe devolver un mensaje con el ID solicitado si el ID es un número positivo.
   Si el ID es 0 o negativo, debe abortar la solicitud con código 400 (Bad Request).
   Si el ID es mayor que 100, debe abortar la solicitud con código 404 (Not Found).

2. `GET /admin`: Debe verificar si existe un parámetro de consulta 'key'.
   Si 'key' no está presente, debe abortar la solicitud con código 401 (Unauthorized).
   Si 'key' no es igual a 'secret123', debe abortar la solicitud con código 403 (Forbidden).

Esta actividad te enseñará a utilizar la función abort() de Flask para manejar
situaciones de error comunes en aplicaciones web.
"""

from flask import Flask, request, abort, jsonify
from werkzeug.routing.converters import IntegerConverter

class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    app.url_map.converters['signed_int'] = SignedIntConverter

#    @app.route('/resource/<int:resource_id>', methods=['GET'])
    @app.route('/resource/<signed_int:resource_id>', methods=['GET'])
    def get_resource(resource_id):
        """
        Devuelve información sobre un recurso según su ID.
        Utiliza abort() en casos de error:
        - Si el ID es <= 0: abort con código 400 (Bad Request)
        - Si el ID es > 100: abort con código 404 (Not Found)
        """
        # Implementa este endpoint utilizando abort() según las condiciones
        #pass

        print(f"Id: {str(resource_id)}")
        if resource_id <= 0:
            abort(400)
        if resource_id > 100:
            abort(404)
        # antes de enviar el id, he dde forzar el cast a string.
        return str(resource_id), 200

    @app.route('/admin', methods=['GET'])
    def admin():
        """
        Endpoint protegido que requiere una clave de acceso.
        Utiliza abort() en casos de error:
        - Si no se proporciona el parámetro 'key': abort con código 401 (Unauthorized)
        - Si la clave no es 'secret123': abort con código 403 (Forbidden)
        """
        # Implementa este endpoint utilizando abort() según las condiciones
        #pass
        params = request.args
        if params.get('key') is None:
            abort(401)
        if params.get('key') != 'secret123':
            abort(403)
        return jsonify(""), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
