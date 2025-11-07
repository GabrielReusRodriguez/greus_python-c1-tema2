"""
Enunciado:
Desarrolla una aplicación web con Flask que demuestre diferentes formas de acceder a la
información enviada en las solicitudes HTTP. Esta aplicación te permitirá entender cómo
procesar diferentes tipos de datos proporcionados por los clientes.

Tu aplicación debe implementar los siguientes endpoints:

1. `GET /headers`: Devuelve los encabezados (headers) de la solicitud en formato JSON.
   - Muestra información como User-Agent, Accept-Language, etc.

2. `GET /browser`: Analiza el encabezado User-Agent y devuelve información sobre:
   - El navegador que está usando el cliente
   - El sistema operativo
   - Si es un dispositivo móvil o no

3. `POST /echo`: Acepta cualquier tipo de datos y devuelve exactamente los mismos datos
   en la misma forma que fueron enviados. Debe manejar:
   - JSON
   - Datos de formulario (form data)
   - Texto plano

4. `POST /validate-id`: Valida un documento de identidad según estas reglas:
   - Debe recibir un JSON con un campo "id_number"
   - El ID debe tener exactamente 9 caracteres
   - Los primeros 8 caracteres deben ser dígitos
   - El último carácter debe ser una letra
   - Devuelve JSON indicando si es válido o no

Esta actividad te enseñará cómo acceder y manipular datos de las solicitudes HTTP,
una habilidad fundamental para crear APIs robustas y aplicaciones web interactivas.
"""

from flask import Flask, jsonify, request
import re

import werkzeug

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/headers', methods=['GET'])
    def get_headers():
        """
        Devuelve los encabezados (headers) de la solicitud en formato JSON.
        Convierte el objeto headers de la solicitud en un diccionario.
        """
        # Implementa este endpoint:
        # 1. Accede a los encabezados de la solicitud usando request.headers
        # 2. Convierte los encabezados a un formato adecuado para JSON
        # 3. Devuelve los encabezados como respuesta JSON
        
        list_of_headers = request.headers
        headers_json = {}
        for item in list_of_headers.items():
            # Nos devuelve una lista de tuplas por lo que la posicion 0 de la tupla es el name del header y la 1 es el valor.
            headers_json[item[0]] = item[1]
        print(f"DEBUUUUUUUUUUUG: {headers_json}")
        return jsonify(headers_json), 200

    @app.route('/browser', methods=['GET'])
    def get_browser_info():
        """
        Analiza el encabezado User-Agent y devuelve información sobre el navegador,
        sistema operativo y si es un dispositivo móvil.
        """
        # Implementa este endpoint:
        # 1. Obtén el encabezado User-Agent de request.headers
        # 2. Analiza la cadena para detectar:
        #    - El nombre del navegador (Chrome, Firefox, Safari, etc.)
        #    - El sistema operativo (Windows, macOS, Android, iOS, etc.)
        #    - Si es un dispositivo móvil (detecta cadenas como "Mobile", "Android", "iPhone")
        # 3. Devuelve la información como respuesta JSON
        #pass
        user_agent = request.headers.get('User-Agent')
        if user_agent is None:
            return jsonify({'error': 'Header User-Agent NOT found'}), 400
        """
            El formato del user agent suele ser: 
            User-Agent: Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>
        """
        agent = {}
        print(f"User-Agent: {user_agent}")
        # Lo intento con una expresion regular. pongo el ^al inicio para indicar que  la expresion debe comenzar con... y $ al final para indicar que debe acabar ahi.
        regexp = r'^([\w\/\d\.]+) \(([\w\d; :\.]+)\) ([\w\d \/\.]+) (\([\w, ]+)\) ([\w\/\. ]+)*'
        
        #^([\w\/\d\.]+) \([\w\d; :\.]+\) ([\w\d \/\.]+)$
        results = re.search(regexp, user_agent)
        if results is None:
            return jsonify({'error': 'Header User-Agent format is NOT correct'}), 400
        #for result in results.:
        #    print(f"HIT!! : {result}")
        groups = results.groups()
        for group in groups:
            if 'browser' not in agent:
                if 'Chrome' in group:
                    agent['browser'] = 'Chrome'
                    continue
                if 'Firefox' in group:
                    agent['browser'] = 'Firefox'
                    continue
                if 'Edge' in group:
                    agent['browser'] = 'Edge'
                    continue
                if 'Safari' in group:
                    agent['browser'] = 'Safari'
                    continue
            if 'os' not in agent:
                if 'Linux' in group:
                    agent['os'] = 'Linux'
                    continue
                if 'Windows' in group:
                    agent['os'] = 'Windows'
                    continue
                if 'iOS' in group:
                    agent['os'] = 'iOS'
                    continue
                if 'Android' in group:
                    agent['os'] = 'Android'
                    continue
                if 'Apple' in group:
                    agent['os'] = 'iOS'
            if 'is_mobile' not in agent:
                if 'Android' in group:
                    agent['is_mobile'] = True
                    continue
                if 'iPhone' in group:
                    agent['is_mobile'] = True
                    continue
                if 'Mobile' in group: 
                    agent['is_mobile'] = True
                    continue
        if 'is_mobile' not in agent:
            agent['is_mobile'] = False
        # Check sistema operativo.
        print(f" result end {results.groups()}")
        return jsonify(agent), 200
        #return jsonify({'msg': 'ok'}), 200

    @app.route('/echo', methods=['POST'])
    def echo():
        """
        Devuelve exactamente los mismos datos que recibe.
        Debe detectar el tipo de contenido y procesarlo adecuadamente.
        """
        # Implementa este endpoint:
        # 1. Detecta el tipo de contenido de la solicitud con request.content_type
        # 2. Según el tipo de contenido, extrae los datos:
        #    - Para JSON: usa request.get_json()
        #    - Para form data: usa request.form
        #    - Para texto plano: usa request.data
        # 3. Devuelve los mismos datos con el mismo tipo de contenido
        #pass
        content_type = request.content_type
        if 'application/json' in content_type:
            return jsonify(request.get_json()), 200, {'Content-Type': content_type}
        if 'multipart/form-data' in content_type:
            return request.form, 200, {'Content-Type': content_type}
        if 'form-urlencoded' in content_type:
            return request.form, 200, {'Content-Type': content_type}
        if 'text/plain' in content_type:
            return request.data, 200, {'Content-Type' : content_type}
        

    @app.route('/validate-id', methods=['POST'])
    def validate_id():
        """
        Valida un documento de identidad según reglas específicas:
        - Debe tener exactamente 9 caracteres
        - Los primeros 8 caracteres deben ser dígitos
        - El último carácter debe ser una letra
        """
        # Implementa este endpoint:
        # 1. Obtén el campo "id_number" del JSON enviado
        # 2. Valida que cumpla con las reglas especificadas
        # 3. Devuelve un JSON con el resultado de la validación
        #pass
        json_data = request.get_json()
        if json_data is None:
            return jsonify({'error': 'JSON Not Found in request'}), 400
        if 'id_number' not in json_data:
            return jsonify({'error': 'JSON in request is not correct'}), 400
        regexp =  r'^\d{8}[a-zA-Z]$'
        match = re.match(regexp, json_data['id_number'])
        if match is None:
            return jsonify({'valid': False}), 200
        return jsonify({'valid': True}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
