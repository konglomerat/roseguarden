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


class ChangePassword(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri='changePassword')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute change password action")
        if user is not None:
            if user.checkPassword(action['oldpassword']):
                user.password = action['newpassword']
                notification_action = webclientActions.NotificationAction.generate("Password changed", "success")
            else:
                notification_action = webclientActions.NotificationAction.generate("Wrong current password!", "error")

        else:
            notification_action = webclientActions.NotificationAction.generate("Internal error (user not found)",
                                                                               "error")

        return 'success', [notification_action]
