"""
Enunciado:
Desarrolla una aplicación web con Flask que utilice Blueprints para organizar las rutas.
Los Blueprints son una característica de Flask que permite organizar una aplicación en componentes modulares y reutilizables.

Tu tarea es implementar una aplicación con dos blueprints:

1. Blueprint 'main': Para las rutas principales
   - `GET /`: Devuelve un mensaje de bienvenida en texto plano.
   - `GET /about`: Devuelve información sobre la aplicación en texto plano.

2. Blueprint 'user': Para las rutas relacionadas con usuarios
   - `GET /user/profile/<username>`: Devuelve un perfil de usuario personalizado en texto plano.
   - `GET /user/list`: Devuelve una lista de usuarios de ejemplo en texto plano.

Además, debes:
   - Registrar ambos blueprints en la aplicación principal
   - Configurar un prefijo URL '/api/v1' para todas las rutas

Esta estructura refleja cómo se organizan las aplicaciones Flask más grandes y complejas,
separando la lógica en componentes modulares que pueden desarrollarse y mantenerse de manera independiente.
"""

from flask import Flask, Blueprint, jsonify


def create_app():
   """
    Crea y configura la aplicación Flask
   """
   app = Flask(__name__)

   # Crea el blueprint 'main'
   main_blueprint = Blueprint('main', __name__)

    # Define las rutas para el blueprint 'main'
   # Implementa las rutas '/' y '/about' para el blueprint 'main'
   @main_blueprint.route('/', methods=['GET'])
   def main_v1():
      return 'Bienvenida', 200, {'Content-Type' : 'text/plain'}

   @main_blueprint.route('/about', methods=['GET'])
   def about_v1():
      return 'Esta es una aplicacion about', 200, {'Content-Type' : 'text/plain'}

   # Crea el blueprint 'user'
   user_blueprint = Blueprint('user', __name__)

   # Define las rutas para el blueprint 'user'
   # Implementa las rutas '/user/profile/<username>' y '/user/list' para el blueprint 'user'
   @user_blueprint.route('/user/profile/<username>', methods=['GET'])
   def user_profile_v1(username):
      return jsonify({'user' : username , 'id' : 1}), 200, {'Content-Type' : 'application/json'}

   
   @user_blueprint.route('/user/list', methods=['GET'])
   def user_list_v1():
      list_user = []
      list_user.append({'user' : 'Gabriel', 'id' : 1})
      list_user.append({'user' : 'Gregorio', 'id' : 2})
      return jsonify(list_user), 200, {'Content-Type' : 'application/json'}


   # Registra los blueprints con un prefijo de URL '/api/v1'
   # Usa app.register_blueprint() con el parámetro url_prefix
   app.register_blueprint(main_blueprint, url_prefix= '/api/v1')
   app.register_blueprint(user_blueprint, url_prefix= '/api/v1')
   return app

# Este seria el run de los apuntes.
if __name__ == '__main__':
   app = create_app()
   app.run(debug=True)
