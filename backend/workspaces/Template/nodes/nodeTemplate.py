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
__contact__ =  "roseguarden@fabba.space"
__credits__ = []
__license__ = "GPLv3"

from app.nodes.nodeClass import NodeClass
from app.nodes.errors import MissingPropertyError
from app.logs import logManager
from app.users import userManager
from workspaces.Template.nodes.common.serverActionRequests import UpdateUserInfoAction, UpdateAssignInfoAction, RequestPinAction, DenyAccessAction, GrandAccessAction
from app.users.enum import AuthenticatorSendBy, AuthenticatorType, AuthenticatorValidityType

class NodeTemplate(NodeClass):

    class_id = "00:01:AB:EF:19:D8:00:11"
    description = "A template node class"

    def defineNodeActionRequests(self):
        # general node action request       
        self.defineNodeActionRequest("registerNodeStartup")
        self.defineNodeActionRequest("requestNodeUpdate")

        # node specific action request       
        self.defineNodeActionRequest("checkAuthenticator")
        self.defineActionProperty("checkAuthenticator", "auth_key") 

        self.defineNodeActionRequest("requestAssignCode")
        self.defineActionProperty("requestAssignCode", "auth_key") 

        self.defineNodeActionRequest("requestUserInfo")
        self.defineActionProperty("requestUserInfo", "auth_key") 

        self.defineNodeActionRequest("requestUserAccess")
        self.defineActionProperty("requestUserAccess", "auth_key") 
        self.defineActionProperty("requestUserAccess", "pin", optional=True) 

    def handleNodeActionRequest(self, action, header):
        logManager.info("handleNodeActionRequest for {}".format(self.name))
        action_name = action['action']
        if action_name == "requestNodeUpdate":
            return [{}]
        elif action_name == "requestUserInfo":
            node_action = UpdateUserInfoAction.generate(userManager.getUserByAuthenticator(action['auth_key']))
            return [node_action]
        elif action_name == "requestUserAccess":
            user = userManager.getUserByAuthenticator(action['auth_key'])
            if user is None:
                return [DenyAccessAction.generate("Access denied", "")]
            
            if userManager.getUserRemainingPinAttempts(user.email) <= 0:
                return [DenyAccessAction.generate("Access denied", "Pin locked")]

            if 'pin' not in action:
                return [RequestPinAction.generate()]
            else:
                if action['pin'] == None or action['pin'] == "":
                    return [RequestPinAction.generate()]
            pinValid = userManager.checkUserPin(user.email, action['pin'])

            if pinValid is False:
                remaining = userManager.getUserRemainingPinAttempts(user.email)
                return [DenyAccessAction.generate("Wrong pin", "Remaining attempts: " + str(remaining))]

            return [GrandAccessAction.generate(user)]
        elif action_name == "requestAssignCode":
            if userManager.checkUserAuthenticatorExists(action['auth_key']) is True:
                node_action = UpdateAssignInfoAction.generate("", False)
            else:
                code = userManager.createUserAuthenticatorRequest(action['auth_key'], 
                                                                    AuthenticatorType.USER,
                                                                    AuthenticatorValidityType.ONCE,
                                                                    AuthenticatorSendBy.NODE,
                                                                    self.identity['nodename'])
                node_action = UpdateAssignInfoAction.generate(code, True)
            return [node_action]
        else:
            return [{}]

        