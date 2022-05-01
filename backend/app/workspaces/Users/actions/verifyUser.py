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
from core.users.models import User


class VerifyUser(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri='verifyUser')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Request user verification")
        user = User.query.filter_by(email=action.email).first()
        if user is None:
            raise Exception("User not found")
        else:
            user.account_verified = True
        return 'success', []

    @staticmethod
    def generate(**kwargs):
        return kwargs
