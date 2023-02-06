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

from flask import request
from core.actions.action import Action
from core.actions import generateActionLink
from core.logs import logManager
from core.actions import webclientActions
from core.users import userManager
from core.messages import send_mail


class ResendVerificationRequest(Action):
    def __init__(self, app):
        super().__init__(app, uri="resendVerificationMail")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute resend activation mail action")
        notification_action = webclientActions.NotificationAction.generate(
            "The verification of your account got requested.", "success"
        )
        ref = request.referrer.split("/")
        if ref[0] != "http:" and ref[0] != "https:":
            ref = "/".join(ref[:1])
        else:
            ref = "/".join(ref[:3])

        verifyUser = userManager.getUser(action.username)
        if verifyUser is not None:
            link = generateActionLink(
                workspace, "verifyUser", {"email": verifyUser.email}, "user/login", True, False, 24 * 3
            )
            data = {
                "username": verifyUser.firstname + " " + verifyUser.lastname,
                "action_link": link,
            }
            print(link)
            send_mail(
                [verifyUser.email],
                "#Rosenwerk Account verifizieren",
                workspace,
                "requestVerification.mail",
                data,
            )
        return "success", [notification_action]
