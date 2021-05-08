"""A simple instant messaging app.(SERVER)
Copyright © 2021 DCL Team

This file is part of SimpleChat-Server.

SimpleChat-Server is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SimpleChat-Server is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SimpleChat-Server.  If not, see <https://www.gnu.org/licenses/>.
"""
from flask import Response
from utils.singleton import Singleton
from traceback import format_exc
from json import dumps


class ServerAction(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        try:
            answer = self.action(*args, **kwargs)
            self.response = Response(answer, status=200, headers={})
        except Exception as e:
            self.response = Response(dumps({
                'is_failed': True,
                'exception': repr(e),
                'trackback': format_exc(),
            }),
                                     status=500,
                                     headers={})
        return self.response


@Singleton
class ChatServer(object):
    flask_ = None

    def set_flask(self, flask_):
        self.flask_ = flask_

    def run(self, *args, **kwargs):
        if self.flask_ is None:
            raise RuntimeError('Server Not Found!')
        self.flask_.run(*args, **kwargs)

    def add_route(self,
                  route=None,
                  route_name=None,
                  handler=None,
                  methods=None):
        if methods is None:
            methods = ['POST']
        if self.flask_ is None:
            raise RuntimeError('Server Not Found!')
        self.flask_.add_url_rule(route,
                                 route_name,
                                 ServerAction(handler),
                                 methods=methods)
