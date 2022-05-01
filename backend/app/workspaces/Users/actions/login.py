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
import arrow


class Login(Action):
    def __init__(self, app):
        # logManager.info("Login of type Action created")
        super().__init__(app, uri='login')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute login action")
        replyActions = []
        user = (actionManager.userManager.getUser(action['username']))

        if user is not None:
            if user.account_verified is False:
                replyActions.append(
                    webclientActions.NotificationAction.generate("Your account need to be verified before login.",
                                                                 "warning"))
                return 'success', replyActions
            if user.checkPassword(action['password']):
                userManager = actionManager.userManager
                menuBuilder = actionManager.menuBuilder
                # update serverside jwt token
                access_token = userManager.updateAccessToken(action['username'])
                # update menu
                menu = menuBuilder.buildMenu(user)
                # build up
                replyActions.append(webclientActions.UpdateSessionTokenAction.generate(access_token))
                replyActions.append(webclientActions.UpdateMenuAction.generate(menu))
                replyActions.append(webclientActions.NotificationAction.generate("Login successful.", "success"))

                if 'options' in action and 'redirect' in action['options']:
                    if action['options']['redirect'] != "":
                        replyActions.append(webclientActions.RouteAction.generate(action['options']['redirect'], 2))
                    else:
                        replyActions.append(webclientActions.RouteAction.generate("dashboard", 2))

                replyActions.append(
                    webclientActions.UpdateUserInfoAction.generate(user.firstname, user.lastname, user.email))
                user.sessionValid = True
                user.last_login_date = arrow.utcnow()
                # actionManager.db.session.commit()
            else:
                replyActions.append(
                    webclientActions.NotificationAction.generate("Login failed, username or password is wrong.",
                                                                 "error"))
        else:
            replyActions.append(
                webclientActions.NotificationAction.generate("Login failed, username or password is wrong.", "error"))

        return 'success', replyActions
