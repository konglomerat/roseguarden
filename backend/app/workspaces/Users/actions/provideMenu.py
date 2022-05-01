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


class ProvideMenu(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri='menu')

    def handle(self, action, user, workspace, actionManager):
        # userManager = actionManager.userManager
        menuBuilder = actionManager.menuBuilder
        logManager.info("Execute registration action")
        menu = menuBuilder.buildMenu(user)
        updateMenu_action = webclientActions.UpdateMenuAction.generate(menu)
        return 'success', [updateMenu_action]
