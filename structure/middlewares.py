from abc import ABC, abstractmethod
from flask import Blueprint, Request, Response


class Middlewares(ABC):
    def __init__(self, req: Request | None):
        self.request: Request = req

    def set_blueprint(self, blueprint: Blueprint):
        blueprint.before_request(self.before)
        blueprint.after_request(self.after)

    @abstractmethod
    def before(self): raise NotImplemented

    @abstractmethod
    def after(self, response: Response): raise NotImplemented
