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
import time
import random
import string
from hashlib import md5, sha1


@Singleton
class GenerateToken(object):

    def generate(self, user_name):
        unix_time = str(round(time.time(), 4))
        md5_salt = ''.join(
            random.sample(string.ascii_letters + string.digits, 8))
        sha1_salt = ''.join(
            random.sample(string.ascii_letters + string.digits, 8))
        token = sha1(
            str(md5().update(
                user_name.encode(encodings="UTF-8") + unix_time + md5_salt)) +
            sha1_salt)
        return token
