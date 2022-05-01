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

from core.actions import executeActionLink
from core.actions.errors import NotFoundError, ExpiredError


class RunActionlink(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri='runActionlink')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute actionlink")
        response_actions = []
        try:
            response_actions.append(webclientActions.UpdateActionlinkStatusAction.generate(
                "success", "Action succeed"))
            response_actions = response_actions + executeActionLink(action.hash, user)
        except (ExpiredError, NotFoundError):
            response_actions = [
                webclientActions.UpdateActionlinkStatusAction.generate("error", "Action not found or expired")
            ]
        except Exception as e:
            logManager.error("Execute actionlink failed: {}".format(str(e)))
            response_actions = [webclientActions.UpdateActionlinkStatusAction.generate("error", "Action failed")]

        return 'success', response_actions
