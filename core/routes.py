from abc import ABC, abstractmethod
from core.server import ChatServer


class Route(ABC):

    def __init__(self, route_name, route):
        self.route_name = route_name
        self.route = route

    @abstractmethod
    def on_post(self):
        raise NotImplementedError

    def register(self, flask_):
        ChatServer().add_route(flask_, self.route, self.route_name,
                               self.on_post)


class TestRoute(Route):

    def __init__(self):
        super().__init__('test', '/test/<fsfs>')

    def on_post(self, fsfs):
        return '<html><head /><body><p>{0}</p></body></html>'.format(fsfs)
