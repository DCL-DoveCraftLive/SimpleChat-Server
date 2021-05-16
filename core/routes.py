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
from json import loads, dumps

from flask import request
from requests import get, Response, post

from utils.config_utils import ConfigParser
from utils.token_utils import Tokens


class Route(ABC):

    def __init__(self, route_name, route):
        self.route_name = route_name
        self.route = route

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class TestRoute(Route):

    def __init__(self):
        super().__init__('test', '/test')

    def __call__(self):
        return str(Tokens().test_all_tokens())


class CheckRoute(Route):

    def __init__(self):
        super().__init__('check_test', '/check/<token>')

    def __call__(self, token):
        a: Tokens = Tokens()
        b = a.check(token)
        return str(b)


class LoginRoute(Route):

    def __init__(self):
        super().__init__('login', '/login')

    def __call__(self):
        data = request.get_data().decode('utf-8')
        data = loads(data)
        if not ('username' in data or 'auth' in data):
            raise ValueError('Wrong Request Format!')
        username, password = data['username'], data['password']

        # 请求用户salt(顺便也验证了用户是否存在)
        url = f"{ConfigParser().get('AuthServer')}/salt/{username}"
        response: Response = get(url)
        response_data = response.json()
        status = response_data['status']
        if status == 0:
            return dumps({
                'status': 0,
                'msg': 'Invalid Username!',
                'token': None,
            })
        if not (status == 0 or status == 1):
            return dumps({
                'status': -1,
                'msg': 'Invalid Status!',
                'token': None,
            })

        # 请求验证
        url = f"{ConfigParser().get('AuthServer')}/login"
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'username': username,
            'password': password,
        }
        response: Response = post(url, headers=headers, data=dumps(payload))
        response_data = response.json()
        status = response_data['status']
        if status == 1:
            return dumps({
                'status': 1,
                'msg': 'Wrong Password!',
                'token': None,
            })
        if not (status == 1 or status == 2):
            return dumps({
                'status': -1,
                'msg': 'Invalid Status!',
                'token': None,
            })
        return dumps({
            'status': 2,
            'msg': 'Success!',
            'token': Tokens().generate(username),
        })


class GetMsgRoute(Route):

    def __init__(self):
        super().__init__('get_msg', '/get_msg')

    def __call__(self):
        raise NotImplementedError()
