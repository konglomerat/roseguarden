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
import arrow
import random
import string
from core.actions.action import Action
from core.logs import logManager
from core.actions import webclientActions
from core.users import userManager
from core.messages import send_mail


class LostPassword(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri='lostPassword')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute lost password action")
        notification_action = webclientActions.NotificationAction.generate(
            "A email to reset the password will be send to you", "success")
        ref = request.referrer.split('/')
        if ref[0] != 'http:' and ref[0] != 'https:':
            ref = '/'.join(ref[:1])
        else:
            ref = '/'.join(ref[:3])

        resetUser = userManager.getUser(action.username)
        if resetUser is not None:
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=96))
            resetUser.password_reset_expired_date = arrow.utcnow().shift(hours=2)
            resetUser.password_reset_hash = key
            link = ref + '/user/resetpassword' + '?key=' + key
            data = {'username': resetUser.firstname + ' ' + resetUser.lastname, 'reset_link': link}
            print(key)
            send_mail([resetUser.email], "Reset your password", workspace, 'lostPassword.mail', data)

        return 'success', [notification_action]
