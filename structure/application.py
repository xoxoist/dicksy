from flask import Flask
from flask import jsonify
from werkzeug.exceptions import HTTPException
from components.controllers import Controllers
from structure import routes_manager
from app.responses import ResponseBase


class ApplicationService:
    """
    "ApplicationService" this represents first entry of the service
    in this class where the merging, initialization, and configs
    are provided and will be distributed between other abstraction.
    """
    __registered_controllers = []
    __config = {
        'port': 5000,
        'debug': 0,
    }

    def add_controller(self, controller: Controllers):
        self.__registered_controllers.append(controller)

    def set_config(self, debug=0, port=5000):
        self.__config = {
            'debug': debug,
            'port': port,
        }

    def log_endpoint(self, app):
        output = []
        for rule in app.url_map.iter_rules():
            if 'GET' in rule.methods and not any(
                    rule.rule.startswith(ignore) for ignore in ['/static', '/favicon.ico']):
                output.append(f"{rule.rule} | {rule.methods}: {rule.endpoint}")
        return output

    def create_app(self):
        app = Flask(__name__)

        app.config["DEBUG"] = self.__config['debug']

        route_extension = routes_manager.RoutesManager(routes=self.__registered_controllers)
        route_extension.register_route(app)

        if app.config['DEBUG'] == 1:
            for t in self.log_endpoint(app):
                print(t)
                pass

        @app.errorhandler(HTTPException)
        def handle_http_exception(e):
            response = ResponseBase()
            response.response_code = "99"
            response.response_message = str(e)
            response_data = jsonify(dict(response))
            response_data.status_code = e.code
            return response_data

        app.run(port=5000)
