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

from core.actions.action import Action
from core.logs import logManager
from core.actions import webclientActions
from core.users import userManager
from core.messages import send_mail, send_message
from core.actions import generateActionLink


class Register(Action):
    def __init__(self, app):
        # logManager.info("Register of type Action created")
        super().__init__(app, uri='register')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute registration action")
        replyActions = []
        userdata = action['userdata']
        if userManager.checkUserExist(userdata['email']):
            replyActions.append(webclientActions.NotificationAction.generate("User already exist", "error"))
        else:
            u = userManager.registerUser(userdata)
            link = generateActionLink(workspace, 'verifyUser', {'email': userdata['email']}, "user/login", True, False)
            data = {'username': userdata['firstname'] + ' ' + userdata['lastname'], 'action_link': link}
            send_mail([userdata['email']], "#Rosenwerk Account verifizieren", workspace, 'requestVerification.mail', data)
            send_message(u, "Welcome", workspace, 'welcome.message', data, 'Roseguarden', False, 'welcome.mail')
            replyActions.append(webclientActions.NotificationAction.generate("User registered", "success"))
            replyActions.append(webclientActions.RouteAction.generate("dashboard", 3))

        return 'success', replyActions
