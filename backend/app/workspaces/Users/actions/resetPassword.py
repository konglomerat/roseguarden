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

import arrow
from core.users.models import User
from core.actions.action import Action
from core.logs import logManager
from core.actions import webclientActions


class ResetPassword(Action):
    def __init__(self, app):
        super().__init__(app, uri='resetPassword')

    def handle(self, action, user, workspace, actionManager):
        user = User.query.filter_by(password_reset_hash=action.resetKey).first()
        if user is None:
            notification_action = webclientActions.NotificationAction.generate("Key is not valid or expired", "error")
        else:
            if user.password_reset_expired_date < arrow.utcnow():
                notification_action = webclientActions.NotificationAction.generate("Key is not valid or expired",
                                                                                   "error")
            else:
                notification_action = webclientActions.NotificationAction.generate("Password changed", "success")
                user.password = action.password

        logManager.info("Request password reset", user)
        return 'success', [notification_action]
