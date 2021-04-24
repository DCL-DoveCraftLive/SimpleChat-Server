from abc import ABC, abstractmethod
from core.server import ChatServer


class Route(ABC):

    def __init__(self, route_name):
        self.route_name = route_name
        self.route = '/{0}'.format(route_name)

    @abstractmethod
    def on_post(self):
        raise NotImplementedError

    def register(self, flask_):
        ChatServer().add_route(flask_, self.route, self.route_name,
                               self.on_post)


class TestRoute(Route):

    def on_post(self):
        return '<html><head /><body><p>111</p></body></html>'
