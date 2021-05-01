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
from yaml import full_load
from traceback import format_exc


@Singleton
class ConfigParser(object):

    def __init__(self):
        self.config_data: dict
        try:
            with open('config.yml') as f:
                self.config_data = full_load(f)
        except Exception as e:
            self.config_data = {
                'is_failed': True,
                'exception': repr(e),
                'traceback': format_exc(),
            }

    def get(self, key):
        if 'is_failed' in self.config_data:
            if self.config_data:
                raise RuntimeError("Cannot Read From 'config.yml'!")
        if key not in self.config_data:
            raise RuntimeError(f"Cannot Find Key '{key}'!")
        return self.config_data[key]
