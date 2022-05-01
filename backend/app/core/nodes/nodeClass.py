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

from enum import Enum
from core.nodes.errors import RequestError


class NodeStatus(Enum):
    UNKNOWN = "UNKNOWN"


class NodeClass(object):
    """Base class that each node class have to inherit from.
       The class define methods that all nodes must implement
    """

    disable = False  # enable or disable detection
    name = None  # overwrites the name (default = self.__class__.__name__)
    class_id = ""  # the nodes class identifier to map hardware nodes with the node class
    description = "UNKNOWN"
    version = "1.0"  # version of the node this class should handle

    def __init__(self, class_id=class_id, name=name):
        self.description = 'UNKNOWN'
        if name is None:
            self.name = self.__class__.__name__
        self.status = NodeStatus.UNKNOWN
        self.actions = {}
        self.defineNodeActionRequests()
        self.identity = {}

    def init_node(self, app, db):
        self.app = app
        self.db = db

    def defineActionProperty(self, actionname, property_name, optional=False, description=""):
        self.actions[actionname]['properties'].append(property_name)
        self.actions[actionname]['optional'] = optional

    def defineNodeActionRequest(self, name, description=""):
        action = {'name': name, 'properties': []}
        action['description'] = description
        self.actions[name] = action

    def check_actions_available(self, action_names_list):
        for n in action_names_list:
            if n not in self.actions:
                raise RequestError("Action " + str(n) + " not available for this node class")
        return True

    def defineNodeActionRequests(self):
        pass

    def defineNodeEvents(self):
        pass

    def defineSettings(self):
        pass

    def handleNodeActionRequest(self, node, action, header):
        pass
