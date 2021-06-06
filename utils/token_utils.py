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

from utils.config_utils import ConfigParser
from utils.singleton import Singleton
from utils.sqlite_utils import SqlParser

TOKEN_EXPIRATION_TIME = ConfigParser().get('TokenExpirationTime')


@Singleton
class Tokens(object):

    def __init__(self):
        self.sql: SqlParser = SqlParser()
        self.sql.init('token').execute('''CREATE TABLE IF NOT EXISTS TOKENS
              (
                  TOKEN     TEXT PRIMARY KEY NOT NULL,
                  TIME      FLOAT            NOT NULL,
                  USER_NAME TEXT             NOT NULL
              );''').end()

    @property
    def tokens(self):
        return self.sql.init('token').execute('''SELECT * FROM TOKENS;''',
                                              is_query=True).end().query_result

    def generate(self, user_name: str):
        """生成一个token

        token生成逻辑:
          1.生成两个盐;\n
          2.对用户名+当前的unix时间+盐进行一次md5;\n
          3.对上一次md5的结果加上第二个盐进行一次sha1.

        Args:
            user_name (str): 要生成token的用户名.
        Returns:
            一个字符串格式的token.
        """
        unix_time = round(time.time(), 4)
        md5_salt = ''.join(
            random.sample(string.ascii_letters + string.digits, 8))
        sha1_salt = ''.join(
            random.sample(string.ascii_letters + string.digits, 8))
        token = sha1((md5((user_name + str(unix_time) +
                           md5_salt).encode(encoding="utf-8")).hexdigest() +
                      sha1_salt).encode(encoding='utf-8')).hexdigest()
        self.sql.init('token').execute(
            f'''INSERT INTO TOKENS (TOKEN, TIME, USER_NAME)
                            VALUES (?,     ?,    ?);''',
            data=[token, unix_time, user_name]).end()
        return token

    def check(self, token) -> bool:
        return round(time.time(), 4) - self.sql.init('token').execute(
            '''SELECT TIME FROM TOKENS WHERE TOKEN = ?''',
            is_query=True,
            data=[token
                 ]).end().query_result[0][0] < TOKEN_EXPIRATION_TIME if len(
                     self.sql.init('token').execute(
                         '''SELECT * FROM TOKENS WHERE TOKEN = ?;''',
                         is_query=True,
                         data=[token]).end().query_result) else False

    def invalidate(self, token) -> bool:
        if not len(
                self.sql.init('token').execute(
                    '''SELECT * FROM TOKENS WHERE TOKEN = ?;''',
                    is_query=True,
                    data=[token]).end().query_result):
            return False
        self.sql.init('token').execute(
            '''DELETE FROM TOKENS WHERE TOKEN = ?;''', data=[token]).end()
        return True

    def update(self, token) -> str:
        """更新一个token

        若token不存在,返回"Unknown Token!".\n
        若token已过期,返回"Invalid Token!",并将无效token删除.\n
        若token未过期,更新token时间.

        Args:
            token (str): 要更新的token.
        Returns:
            "Unknown Token!"或"Invalid Token!"或一个新token
        """
        if not len(
                self.sql.init('token').execute(
                    '''SELECT * FROM TOKENS WHERE TOKEN = ?;''',
                    is_query=True,
                    data=[token]).end().query_result):
            return 'Unknown Token!'
        if self.check(token):
            user_name = self.sql.init('token').execute(
                '''SELECT USER_NAME FROM TOKENS WHERE TOKEN = ?;''',
                is_query=True,
                data=[token]).end().query_result
            self.invalidate(token)
            return self.generate(user_name)
        else:
            self.sql.init('token').execute(
                '''UPDATE TOKENS SET TIME = ? WHERE TOKEN = ?;''',
                data=[round(time.time(), 4), token]).end()
            return 'Updated!'

    def test_all_tokens(self):
        return self.tokens
