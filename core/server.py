from flask import Response
from utils.singleton import Singleton
from traceback import format_exc
from json import dumps


class ServerAction(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        try:
            answer = self.action()
            self.response = Response(answer, status=200, headers={})
        except Exception:
            self.response = Response(dumps({'error': format_exc()}),
                                     status=500,
                                     headers={})
        return self.response


@Singleton
class ChatServer(object):

    # def __init__(self, flask_: Flask):
    #     self.flask_ = flask_

    def run(self, flask_, *args, **kwargs):
        flask_.run(*args, **kwargs)

    def add_route(self, flask_, route=None, route_name=None, handler=None):
        flask_.add_url_rule(route,
                            route_name,
                            ServerAction(handler),
                            methods=['POST', 'GET'])
