from flask import Flask
from structure import controllers
from structure import routes_manager


class ApplicationService:
    """
    "ApplicationService" this represents first entry of the service
    in this class where the merging, initialization, and configs
    are provided and will be distributed between other abstraction.
    """
    __registered_controllers = []

    def add_controller(self, controller: controllers.Controllers):
        self.__registered_controllers.append(controller)

    def create_app(self):
        app = Flask(__name__)
        app.config["ERROR_404_HELP"] = False
        route_extension = routes_manager.RoutesManager(routes=self.__registered_controllers)
        route_extension.register_route(app)
        return app
