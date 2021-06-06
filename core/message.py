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
from utils.singleton import Singleton
from utils.sqlite_utils import SqlParser
from utils.token_utils import Tokens


@Singleton
class Messages(object):

    def __init__(self):
        self.sql: SqlParser = SqlParser()
        self.sql.init('msg').execute('''CREATE TABLE IF NOT EXISTS MESSAGES
            (
                ID        INTEGER PRIMARY KEY NOT NULL,
                USER_NAME TEXT                NOT NULL,
                GROUP_ID  INTEGER             NOT NULL,
                RAW_MSG   TEXT                NOT NULL
            );''').end()

    def get(self, num):
        return self.sql.init('msg').execute(
            '''SELECT * FROM MESSAGES''',
            is_query=True).end().query_result[-num::]

    def send(self, msg, group_id, token):
        if Tokens().check(token):
            user_name = self.sql.init('token').execute(
                '''SELECT USER_NAME FROM TOKENS WHERE TOKEN = ?;''',
                is_query=True,
                data=[token]).end().query_result[0][0]
            # id_ = self.get(1)[0][2] + 1
            self.sql.init('msg').execute(
                '''INSERT INTO MESSAGES (USER_NAME, GROUP_ID, RAW_MSG)
                               VALUES   (?,         ?,        ?);''',
                data=[user_name, group_id, msg]).end()
