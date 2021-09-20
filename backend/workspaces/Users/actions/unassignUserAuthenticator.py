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

from core.users.models import User
from core.users.enum import UserAuthenticatorStatus
from core.actions.action import Action
from core.logs import logManager
from core.actions import webclientActions


class UnassignUserAuthentictor(Action):
    def __init__(self, app):
        super().__init__(app, uri='unassignUserAuthenticator')

    def handle(self, action, user, workspace, actionManager):
        user_to_unassign = User.query.filter_by(email=action.userId).first()
        notification_action = webclientActions.NotificationAction.generate("Assign authenticator was succesful.",
                                                                           "success")

        if user is None:
            notification_action = webclientActions.NotificationAction.generate(
                "You have to be logged in to do this action.", "error")
            return 'success', [notification_action], {
                'succeed': False,
                'message': "You have to be logged in to do this action."
            }

        logManager.info("Request for authenticator unassign for {} by {}".format(action.userId, user.email))

        if user_to_unassign is None:
            notification_action = webclientActions.NotificationAction.generate(
                "Failed to unassign authenticator to user.", "error")
            return 'success', [notification_action], {
                'succeed': False,
                'message': "Failed to unassign authenticator to user."
            }

        # other user can only set authenticator if not already set
        if user.email != user_to_unassign.email:
            if user_to_unassign.authenticator_status is not UserAuthenticatorStatus.UNSET:
                notification_action = webclientActions.NotificationAction.generate(
                    "Failed to unassign authenticator to user", "error")
                return 'success', [notification_action], {
                    'succeed': False,
                    'message': "Failed to unassign authenticator."
                }

        user_to_unassign.resetAuthenticator()
        user_to_unassign.authenticator_status = UserAuthenticatorStatus.UNSET

        return 'success', [notification_action], {'succeed': True, 'message': "Assign successful"}
