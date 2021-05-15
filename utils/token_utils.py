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
import random
import string
import time
from hashlib import md5, sha1

from utils.singleton import Singleton
from utils.sqlite_utils import SqlParser


def get_tokens() -> list:
    result = SqlParser().init('token').execute(
        '''SELECT * FROM TOKENS;''', is_query=True).end().query_result
    return result


@Singleton
class Tokens(object):

    def __init__(self):
        SqlParser().init('token').execute('''CREATE TABLE IF NOT EXISTS TOKENS
              (
                  TOKEN     TEXT PRIMARY KEY NOT NULL,
                  TIME      FLOAT            NOT NULL,
                  USER_NAME TEXT             NOT NULL
              );''').end()
        self.tokens = get_tokens()

    def generate(self, user_name: str):
        unix_time = round(time.time(), 4)
        md5_salt = ''.join(
            random.sample(string.ascii_letters + string.digits, 8))
        sha1_salt = ''.join(
            random.sample(string.ascii_letters + string.digits, 8))
        token = sha1(
            str(
                md5((user_name + str(unix_time) +
                     md5_salt).encode(encoding="utf-8")).hexdigest() +
                sha1_salt).encode(encoding='utf-8')).hexdigest()
        SqlParser().init('token').execute(
            f'''INSERT INTO TOKENS (TOKEN, TIME, USER_NAME)
                            VALUES (?,     ?,    ?);''',
            data=(token, unix_time, user_name)).end()
        self.tokens = get_tokens()
        return token

    def check(self, token) -> bool:
        self.tokens = get_tokens()
        for i in self.tokens:
            if token in i:
                if time.time() - i[1] > 21600.0:
                    return True
        return False

    def update(self, token) -> bool:
        self.tokens = get_tokens()
        for i in self.tokens:
            if token in i:
                SqlParser().init('token').execute(
                    '''UPDATE TOKENS SET TIME = ? WHERE TOKEN = ?;''',
                    data=(round(time.time(), 4), token))
        return True

    def test(self):
        self.tokens = get_tokens()
        return self.tokens
