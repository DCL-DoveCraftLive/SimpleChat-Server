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
from yaml import full_load, dump


@Singleton
class ConfigParser(object):

    def __init__(self):
        self.config_data: dict
        with open('config.yml', 'r') as f:
            self.config_data = full_load(f)

    def get(self, key):
        if 'is_failed' in self.config_data:
            if self.config_data:
                raise RuntimeError("Cannot Read From 'config.yml'!")
        if key not in self.config_data:
            raise RuntimeError(f"Cannot Find Key '{key}'!")
        return self.config_data[key]

    def __flush(self):
        with open('config.yml', 'w') as f:
            dump(self.config_data, f)

    def set_(self, key, value):
        self.config_data[key] = value
        self.__flush()
