"""
The roseguarden project

Copyright (C) 2018-2020  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "roseguarden@fabba.space"
__credits__ = []
__license__ = "GPLv3"

import json


class RegisterNodeStartup():
    def __init__(self, action_id=1):
        self.action = 'registerNodeStartup'
        self.actionid = action_id
        self.version = '1.0.0'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class RequestUserAccess():
    def __init__(self, auth_key, action_id=1):
        self.action = 'requestUserAccess'
        self.actionid = action_id
        self.version = '1.0.0'
        self.auth_key = auth_key

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
