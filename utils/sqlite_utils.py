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
import os
import sqlite3

from utils.singleton import Singleton


@Singleton
class SqlParser(object):

    def __init__(self):
        # 可以为'file'或'mem'
        self.target_db: str = 'file'
        self.__initialized = False
        self.db_connection = None
        self.db_cursor = None
        self.query_result = None

    def set_target(self, target):
        if target not in ['msg', 'mem']:
            raise RuntimeError('Unknown Database!')
        if not target == self.target_db:
            self.target_db = target
        return self

    def init(self, db_name=None):
        if self.target_db == 'mem' and db_name is not None:
            raise ValueError('Invalid Name!')
        target = ':memory:'
        if self.target_db == 'file':
            target = f'data{os.sep}{db_name}.db'
        self.db_connection: sqlite3.Connection = sqlite3.connect(target)
        self.db_cursor: sqlite3.Cursor = self.db_connection.cursor()
        self.__initialized = True
        return self

    def end(self):
        self.db_connection.commit()
        self.db_cursor.close()
        self.db_connection.close()
        self.db_cursor, self.db_connection = None, None
        self.__initialized = False
        if self.query_result is not None:
            return self
        else:
            self.query_result = None

    def execute(self, statement, is_query=False):
        self.db_cursor.execute(statement)
        if is_query:
            self.query_result = self.db_cursor.fetchall()
        return self
