"""
Enunciado:
Desarrolla una aplicación web con Flask que procese diferentes tipos MIME (Multipurpose Internet Mail Extensions)
recibidos en solicitudes HTTP. Esta aplicación te permitirá entender cómo recibir y procesar
diferentes formatos de datos enviados por los clientes.

Los tipos MIME son fundamentales en el desarrollo web ya que indican cómo interpretar los datos
recibidos en las solicitudes HTTP. Una API robusta debe poder manejar diversos formatos de entrada.

Tu aplicación debe implementar los siguientes endpoints:

1. `POST /text`: Recibe un texto plano con el tipo MIME `text/plain` y lo devuelve en la respuesta.
   - Ejemplo de uso: Procesar mensajes simples o logs enviados por el cliente.

2. `POST /html`: Recibe un fragmento HTML con el tipo MIME `text/html` y lo devuelve en la respuesta.
   - Ejemplo de uso: Recibir contenido HTML para almacenar o procesar.

3. `POST /json`: Recibe un objeto JSON con el tipo MIME `application/json` y lo devuelve en la respuesta.
   - Ejemplo de uso: Procesar datos estructurados en APIs RESTful.

4. `POST /xml`: Recibe un documento XML con el tipo MIME `application/xml` y lo devuelve en la respuesta.
   - Ejemplo de uso: Procesar configuraciones o datos estructurados en formato XML.

5. `POST /image`: Recibe una imagen con el tipo MIME `image/png` o `image/jpeg` y la guarda en el servidor.
   - Ejemplo de uso: Subir imágenes para un perfil de usuario o una galería.

6. `POST /binary`: Recibe datos binarios con el tipo MIME `application/octet-stream` y confirma su recepción.
   - Ejemplo de uso: Recibir archivos genéricos como PDFs o archivos comprimidos.

Tu tarea es completar la implementación de la función create_app() y de los endpoints solicitados,
asegurándote de identificar correctamente el tipo MIME de cada solicitud y procesarla adecuadamente.

Esta actividad te enseñará cómo recibir y manejar diferentes tipos de datos en solicitudes HTTP,
una habilidad esencial para desarrollar APIs web que interactúan con diversos clientes.
"""

from flask import Flask, jsonify, request, Response
import os


num_img = 0

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    # Crear un directorio para guardar archivos subidos si no existe
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)

    @app.route('/text', methods=['POST'])
    def post_text():
        """
        Recibe un texto plano con el tipo MIME `text/plain` y lo devuelve en la respuesta.
        """
        # Implementa este endpoint:
        # 1. Verifica que el Content-Type sea text/plain
        # 2. Lee el contenido de la solicitud usando request.data
        # 3. Devuelve el mismo texto con Content-Type text/plain
        #pass
        if request.content_type == 'text/plain':
            return request.data, 200, {'Content-Type' : 'text/plain'}
        else:
            return 'ERROR', 400, {'Content-Type' : 'text/plain'}



    @app.route('/html', methods=['POST'])
    def post_html():
        """
        Recibe un fragmento HTML con el tipo MIME `text/html` y lo devuelve en la respuesta.
        """
        # Implementa este endpoint:
        # 1. Verifica que el Content-Type sea text/html
        # 2. Lee el contenido de la solicitud
        # 3. Devuelve el mismo HTML con Content-Type text/html
        #pass
        if request.content_type == 'text/html':
            return request.data, 200, {'Content-Type' : 'text/html'}
        else:
            return '<html><head/><body>ERROR</body></html>', 400, {'Content-Type' : 'text/html'}


    @app.route('/json', methods=['POST'])
    def post_json():
        """
        Recibe un objeto JSON con el tipo MIME `application/json` y lo devuelve en la respuesta.
        """
        # Implementa este endpoint:
        # 1. Accede al contenido JSON usando request.get_json()
        # 2. Devuelve el mismo objeto JSON usando jsonify()
        #pass
        _data = request.get_json()
        return jsonify(_data), 200, {'Content-Type' : 'application/json'}

    @app.route('/xml', methods=['POST'])
    def post_xml():
        """
        Recibe un documento XML con el tipo MIME `application/xml` y lo devuelve en la respuesta.
        """
        # Implementa este endpoint:
        # 1. Verifica que el Content-Type sea application/xml
        # 2. Lee el contenido XML de la solicitud
        # 3. Devuelve el mismo XML con Content-Type application/xml
        #pass
        if request.content_type == 'application/xml':
            return request.data, 200, {'Content-Type' : 'application/xml'}
        else:
            return '<mensaje>ERROR</mensaje>', 400, {'Content-Type' : 'application/xml'}


    @app.route('/image', methods=['POST'])
    def post_image():
        """
        Recibe una imagen con el tipo MIME `image/png` o `image/jpeg` y la guarda en el servidor.
        """
        # Implementa este endpoint:
        # 1. Verifica que el Content-Type sea image/png o image/jpeg
        # 2. Lee los datos binarios de la imagen
        # 3. Guarda la imagen en el directorio 'uploads' con un nombre único
        # 4. Devuelve una confirmación con el nombre del archivo guardado
        #pass
        global num_img
        if request.content_type == 'image/png' or request.content_type == 'image/jpeg':
            _img_data = request.data
            """ Si el directorio existe, hace un raise de FileExistsError ."""
            try:
                os.mkdir('./uploads/')
            except FileExistsError  as e:
                pass
            file_name = 'img' + str(num_img)
            file_path = f'./uploads/{file_name}'
            with open(file_path, 'wb+') as f:
                f.write(_img_data)
            resp = {'mensaje': 'OK', 'archivo': file_path}
            num_img  = num_img + 1
            return  jsonify(resp), 200, {'Content-Type' : 'application/json'}
        else:
            return jsonify({'mensaje' : 'Error'}), 400, {'Content-Type' : 'application/json'}


    @app.route('/binary', methods=['POST'])
    def post_binary():
        """
        Recibe datos binarios con el tipo MIME `application/octet-stream` y confirma su recepción.
        """
        # Implementa este endpoint:
        # 1. Verifica que el Content-Type sea application/octet-stream
        # 2. Lee los datos binarios de la solicitud
        # 3. Guarda los datos en un archivo o simplemente verifica su tamaño
        # 4. Devuelve una confirmación con información sobre los datos recibidos
        #pass
        if request.content_type == 'application/octet-stream':
            _data = request.data
            return jsonify({'mensaje': 'OK', 'tamaño' : len(_data)}), 200, {'Content-Type' : 'application/json'}
        else:
            return jsonify({'mensaje': 'Error'}), 400,{'Content-Type' : 'application/json'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
