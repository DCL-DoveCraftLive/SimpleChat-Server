from flask import Flask, Response
from utils.singleton import Singleton


class ServerAction(object):

    def __init__(self, action):
        self.action = action

    def __call__(self):
        try:
            answer = self.action()
            self.response = Response(answer, status=200, headers={})
        except Exception as e:
            self.response = Response(e, status=500, headers={})
        return self.response


@Singleton
class ChatServer(object):

    def __init__(self, flask_: Flask):
        self.flask_ = flask_

    def run(self, *args):
        self.flask_.run(*args)

    def add_route(self, route=None, route_name=None, handler=None):
        self.flask_.add_url_rule(route, route_name, ServerAction(handler))
