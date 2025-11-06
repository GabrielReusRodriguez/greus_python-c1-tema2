"""
Enunciado:
Desarrolla una API REST utilizando Flask que gestione un catálogo de animales e implemente
manejo de errores personalizado con el decorador @app.errorhandler.

La API debe exponer los siguientes endpoints:

1. `GET /animals`: Devuelve la lista completa de animales.
2. `GET /animals/<animal_id>`: Devuelve la información de un animal específico por su ID.
3. `POST /animals`: Agrega un nuevo animal. El cuerpo debe incluir JSON con campos "name" y "species".
4. `DELETE /animals/<animal_id>`: Elimina un animal específico por su ID.

Además, debes implementar manejadores personalizados para los siguientes errores HTTP:

- 400 (Bad Request): Cuando faltan datos necesarios o tienen formato incorrecto.
- 404 (Not Found): Cuando se solicita un animal que no existe.
- 405 (Method Not Allowed): Cuando se utiliza un método HTTP no permitido.
- 500 (Internal Server Error): Para errores internos del servidor.

Requisitos:
- Implementar los manejadores de errores utilizando el decorador @app.errorhandler.
- Cada manejador debe devolver una respuesta JSON con un mensaje descriptivo y el código de estado correspondiente.
- Asegúrate de que la función delete_animal lance un error 404 cuando se intenta eliminar un animal que no existe.
- Implementa un manejador para el error 500 que registre el error en los logs de la aplicación.

Ejemplo:
- Una solicitud a un endpoint inexistente debe activar el manejador de error 404.
- Una solicitud POST sin los campos requeridos debe activar el manejador de error 400.
- Intentar eliminar un animal inexistente debe activar el manejador de error 404.

Tu tarea es implementar esta API en Flask con el manejo adecuado de errores.
"""

from flask import Flask, jsonify, request, abort
import logging

# Configuración del registro (logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de animales predefinida
animals = [
    {"id": 1, "name": "León", "species": "Panthera leo"},
    {"id": 2, "name": "Elefante", "species": "Loxodonta africana"},
    {"id": 3, "name": "Jirafa", "species": "Giraffa camelopardalis"}
]

# Este contador se usará para asignar IDs únicos
next_id = 4

def create_app():
    """
    Crea y configura la aplicación Flask con manejadores de errores personalizados
    """
    app = Flask(__name__)
    
    # Manejador de errores 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        """
        Maneja errores de solicitud incorrecta (400)
        Devuelve un JSON con mensaje de error y código de estado 400
        """
        # Implementa este manejador de errores
        # 1. Registra el error usando app.logger.warning() con un mensaje descriptivo
        # 2. Devuelve un JSON con un mensaje descriptivo y el código de estado 400
        #pass
        app.logger.warning(str(error))
        return jsonify({'error': str(error)}), 400

    # Manejador de errores 404 - Not Found
    @app.errorhandler(404)
    def not_found(error):
        """
        Maneja errores de recurso no encontrado (404)
        Devuelve un JSON con mensaje de error y código de estado 404
        """
        # Implementa este manejador de errores
        # 1. Registra el error usando app.logger.info() con un mensaje descriptivo
        # 2. Devuelve un JSON con un mensaje descriptivo y el código de estado 404
        #pass
        app.logger.info(str(error))
        return jsonify({'error': str(error)}), 404

    # Manejador de errores 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(error):
        """
        Maneja errores de método no permitido (405)
        Devuelve un JSON con mensaje de error y código de estado 405
        """
        # Implementa este manejador de errores
        # 1. Registra el error usando app.logger.warning() con un mensaje descriptivo
        # 2. Devuelve un JSON con un mensaje descriptivo y el código de estado 405
        #pass
        app.logger.warning(str(error))
        return jsonify({'error': str(error)}), 405

    # Manejador de errores 500 - Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        """
        Maneja errores internos del servidor (500)
        Registra el error en los logs y devuelve un JSON con mensaje de error
        """
        # Implementa este manejador de errores
        # 1. Registra el error usando app.logger.error() con los detalles del error
        # 2. Incluye información adicional como la ruta que causó el error utilizando request.path
        # 3. Devuelve un JSON con un mensaje descriptivo y el código de estado 500
        #pass
        app.logger.error(str(error))
        app.logger.error(f'Path: {request.path}')
        return jsonify({'error': str(error)}), 500

    @app.route('/animals', methods=['GET'])
    def get_animals():
        """
        Devuelve la lista completa de animales
        """
        # Implementa este endpoint para devolver la lista de animales
        #pass
        return jsonify(animals), 200            

    @app.route('/animals/<int:animal_id>', methods=['GET'])
    def get_animal(animal_id):
        """
        Devuelve la información de un animal específico por su ID
        Si el animal no existe, debe activar un error 404
        """
        animal = next((a for a in animals if a['id'] == animal_id), None)
        if animal is None:
            # Si el animal no existe, usa abort(404) para lanzar un error 404
            abort(404)
        return jsonify(animal)

    @app.route('/animals', methods=['POST'])
    def add_animal():
        """
        Agrega un nuevo animal
        El cuerpo debe incluir JSON con campos "name" y "species"
        Si falta algún campo, debe activar un error 400
        """
        # Implementa este endpoint
        # 1. Verifica que el cuerpo de la solicitud contenga JSON
        # 2. Verifica que los campos "name" y "species" estén presentes
        # 3. Si falta algún campo, usa abort(400) para lanzar un error
        # 4. Si todo está correcto, agrega el nuevo animal a la lista y devuelve una respuesta adecuada (código 201)
        #pass
        # indico que next_id es global
        global next_id
        data = request.get_json()
        if data is None:
            abort(400)
        if data.get('name') is None or data.get('species') is None:
            abort(400)
        animal = {}
        animal['id'] = next_id
        animal['name'] = data.get('name')
        animal['species'] = data.get('species')
        animals.append(animal)
        next_id = next_id + 1
        return jsonify(animal), 201, {'Context-Type': 'application/json'}

    @app.route('/animals/<int:animal_id>', methods=['DELETE'])
    def delete_animal(animal_id):
        """
        Elimina un animal específico por su ID
        Si el animal no existe, debe activar un error 404
        """
        # Implementa este endpoint
        # 1. Verifica si el animal existe
        # 2. Si no existe, usa abort(404) para lanzar un error 404
        # 3. Si existe, elimínalo de la lista y devuelve una respuesta adecuada
        #pass
        animal = next((a for a in animals if a.get('id') == animal_id), None)
        if animal is None:
            abort(404)
        # pasamos a borrarlo.
        animals.remove(animal)
        return jsonify(''), 204, {'Context-Tyoe': 'application/json'}

    # Endpoint adicional que lanza un error 500 para probar el manejador
    @app.route('/test-error', methods=['GET'])
    def test_error():
        """
        Endpoint de prueba que lanza un error 500 intencionalmente
        """
        # Lanza una excepción para probar el manejador de error 500
        raise Exception("¡Este es un error de prueba!")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)