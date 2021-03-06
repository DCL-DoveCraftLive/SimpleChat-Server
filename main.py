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
from flask import Flask

from core.routes import *
from core.server import ChatServer

flask_ = Flask(__name__)

server: ChatServer = ChatServer()
server.set_flask(flask_).register(TestRoute(), methods=[
    'GET'
]).register(LoginRoute()).register(CheckRoute(), methods=['GET']).register(
    UpdateRoute(),
    methods=['GET']).register(DefaultGetMsgRoute(), methods=['GET']).register(
        CustomGetMsgRoute(), methods=['GET']).register(SendMsgRoute(),
                                                       methods=['POST', 'GET'])
server.run(debug=True)
