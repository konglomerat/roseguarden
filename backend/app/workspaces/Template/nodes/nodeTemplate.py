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

from core.nodes.nodeClass import NodeClass
from core.logs import logManager
from core.users import userManager
from workspaces.Template.nodes.common.serverActionRequests import UpdateUserInfoAction


class NodeTemplate(NodeClass):

    class_id = "00:01:02:03:04:05:06:07"
    description = "A template node class"

    def defineNodeActionRequests(self):
        # general node action request
        self.defineNodeActionRequest("registerNodeStartup")
        self.defineNodeActionRequest("requestNodeUpdate")

        # node specific action request
        self.defineNodeActionRequest("requestUserInfo")
        self.defineActionProperty("requestUserInfo", "auth_key")

    def handleNodeActionRequest(self, node, action, header):
        logManager.info("handleNodeActionRequest for {}".format(self.name))
        action_name = action['action']
        public_key = ""
        if 'public_key' in action:
            public_key = action['public_key']

        if action_name == "requestNodeUpdate":
            return [{}]
        elif action_name == "requestUserInfo":
            node_action = UpdateUserInfoAction.generate(
                userManager.get_user_by_authenticator(action['auth_key'], public_key))
            return [node_action]
        else:
            return [{}]
