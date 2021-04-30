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
from abc import ABC, abstractmethod
from core.server import ChatServer
from flask import request
from json import loads


class Route(ABC):

    def __init__(self, route_name, route):
        self.route_name = route_name
        self.route = route

    @abstractmethod
    def __call__(self):
        raise NotImplementedError

    def register(self, methods=['POST']):
        ChatServer().add_route(self.route, self.route_name, self, methods)


class TestRoute(Route):

    def __init__(self):
        super().__init__('test', '/test/<fsfs>')

    def __call__(self, fsfs):
        return '<html><head /><body><p>{0}</p></body></html>'.format(fsfs)


class LoginRoute(Route):
    # TODO(shoot@vancraft.cn): finish login function
    def __init__(self):
        super().__init__('login', '/login')

    def __call__(self):
        data = request.get_data().decode('utf-8')
        data = loads(data)
        if not ('username' in data or 'auth' in data):
            raise ValueError('Wrong Request Format!')
