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


class BaseAction(object):
    action = 'undefined'
    target = 'undefined'
    source = 'server'
    version = '1.0.0'

    def __init__(self, ):
        print("Instance of BaseAction created")

    def execute(self, ):
        print("Execute not defined")

    @classmethod
    def generate(cls, delay=0.0):
        action = {}
        action['action'] = cls.action
        action['target'] = cls.target
        action['version'] = cls.version
        action['source'] = cls.source
        action['delay'] = delay
        return action


class BaseNodeAction(object):
    action = 'undefined'
    version = '1.0.0'

    def __init__(self, ):
        print("Instance of BaseAction created")

    def execute(self, ):
        print("Execute not defined")

    @classmethod
    def generate(cls):
        action = {}
        action['action'] = cls.action
        action['version'] = cls.version
        return action
