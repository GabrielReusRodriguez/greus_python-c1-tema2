"""
Enunciado:
Desarrolla una aplicación web básica con Flask que muestre el uso del sistema de registro (logging).

En el desarrollo web es fundamental tener un buen sistema de registro de eventos,
que permita hacer seguimiento de lo que ocurre en nuestra aplicación. Flask proporciona
un objeto logger integrado (app.logger) que permite registrar mensajes con diferentes
niveles de importancia.

Tu tarea es implementar los siguientes endpoints:

1. `GET /info`: Registra un mensaje de nivel INFO y devuelve un mensaje en texto plano.
2. `GET /warning`: Registra un mensaje de nivel WARNING y devuelve un mensaje en texto plano.
3. `GET /error`: Registra un mensaje de nivel ERROR y devuelve un mensaje en texto plano.
4. `GET /critical`: Registra un mensaje de nivel CRITICAL y devuelve un mensaje en texto plano.

Esta actividad te enseñará a utilizar el sistema de registro de Flask,
una habilidad crucial para el desarrollo y depuración de aplicaciones web.
"""

from flask import Flask, jsonify, request

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    # Configuración básica del logger
    # Por defecto, los mensajes se registrarán en la consola

    @app.route('/info', methods=['GET'])
    def log_info():
        """
        Registra un mensaje de nivel INFO
        """
        # Implementa este endpoint:
        # 1. Registra un mensaje de nivel INFO usando app.logger.info()
        # 2. Devuelve un mensaje en texto plano indicando que se ha registrado el mensaje
        #pass not in 
        app.logger.info('registrado GET')
        # La forma simple es devover el texto, el codigo de error y un diccionario con los headers.
        return 'Se ha regitsrado el info.', 200, {'Content-Type': 'text/plain'}

    @app.route('/warning', methods=['GET'])
    def log_warning():
        """
        Registra un mensaje de nivel WARNING
        """
        # Implementa este endpoint:
        # 1. Registra un mensaje de nivel WARNING usando app.logger.warning()
        # 2. Devuelve un mensaje en texto plano indicando que se ha registrado el mensaje
        #pass
        app.logger.warning('registrado get')
        return 'Se ha registrado el warning',200, {'Content-Type': 'text/plain'}

    @app.route('/error', methods=['GET'])
    def log_error():
        """
        Registra un mensaje de nivel ERROR
        """
        # Implementa este endpoint:
        # 1. Registra un mensaje de nivel ERROR usando app.logger.error()
        # 2. Devuelve un mensaje en texto plano indicando que se ha registrado el mensaje
        app.logger.error('registrado get')
        return '  Se ha registrado el error', 200, {'Content-Type': 'text/plain'}

    @app.route('/critical', methods=['GET'])
    def log_critical():
        """
        Registra un mensaje de nivel CRITICAL
        """
        # Implementa este endpoint:
        # 1. Registra un mensaje de nivel CRITICAL usando app.logger.critical()
        # 2. Devuelve un mensaje en texto plano indicando que se ha registrado el mensaje
        app.logger.critical('Registrado get')
        return 'Se ha registrado el critical', 200, {'Content-Type': 'text/plain'}

    @app.route('/status', methods=['GET'])
    def status():
        """
        Endpoint adicional que registra diferentes mensajes según el parámetro de consulta 'level'
        Ejemplo: /status?level=warning
        """
        # Este endpoint es opcional, puedes implementarlo si quieres practicar
        # con parámetros de consulta y logging condicional
        # obtengo los parametros.
        msg = 'Se ha registrado el GET'
        params = request.args
        if  params.get('level') is not None:
            if params.get('level') == 'info':
                app.logger.info(msg)
            if params.get('level') == 'warning':
                app.logger.warning(msg)
            if params.get('level') == 'error':
                app.logger.error(msg)
            if params.get('level') == 'critical':
                app.logger.critical(msg)
        return 'Se ha registrado el msg', 200, { 'Content-Type': 'text/plain'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
