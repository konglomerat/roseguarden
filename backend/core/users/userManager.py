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

import secrets
import datetime
import hashlib
import arrow
from flask_jwt_extended import create_access_token, create_refresh_token

from core.logs import logManager
from core.workspaces.workspaceHooks import WorkspaceHooks


class UserManager(object):
    """ The UserManager ...
    """
    def __init__(self, ):
        # preparation to instanciate
        pass

    def init_manager(self, app, db, workspaceManager, config):
        self.config = config
        self.app = app
        self.db = db
        self.workspaceManager = workspaceManager
        self.pinAttemptLimit = 6
        logManager.info("UserManager initialized")

        from core.users.models import User, Authenticator
        self.user = User
        self.authenticator_request = Authenticator
        self.user_authenticator_cache = {}

    def removeUser(self, email):
        u = self.user.query.filter_by(email=email).first()
        if u is not None:
            self.workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.REMOVEUSER, user=u)
            self.db.session.delete(u)
            self.db.session.commit()

    def registerUser(self, userdata):
        if self.checkUserExist(userdata['email']):
            return None
        else:
            u = self.user(email=userdata['email'].strip().lower(), password=userdata['password'], isAdmin=False)
            if 'firstname' in userdata:
                u.firstname = userdata['firstname']
            if 'lastname' in userdata:
                u.lastname = userdata['lastname']
            if 'organization' in userdata:
                u.organization = userdata['organization']

            self.workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=u)
            self.db.session.add(u)
            self.db.session.commit()
            return u

    def updateUserPassword(self, user, newpassword):
        user.password = newpassword

    def updateAccessToken(self, username):
        session_expiration_minutes = self.config['SYSTEM'].get('session_expiration_minutes', 15)
        exp_delta = datetime.timedelta(minutes=session_expiration_minutes)
        access_token = create_access_token(identity=username, expires_delta=exp_delta)
        create_refresh_token(identity=username)
        return access_token

    def createUserAuthenticatorRequest(self,
                                       authenticator_key,
                                       authenticator_type,
                                       validity_type,
                                       code_send_by,
                                       code_send_to,
                                       expire_days=3):
        token = secrets.token_hex(6)
        print(token)
        code = ':'.join(a + b for a, b in zip(token[::2], token[1::2])).upper()
        print(code)
        a = self.authenticator_request()
        a.authenticator_type = authenticator_type
        a.validity_type = validity_type
        a.expire_date = arrow.utcnow().shift(days=expire_days)
        a.created_date = arrow.utcnow()
        a.code = code
        a.code_send_by = code_send_by
        a.code_send_to = code_send_to
        a.authenticator = authenticator_key
        self.db.session.add(a)
        self.db.session.commit()
        return code

    def getUserByAuthenticator(self, authenticator_key):
        h = hashlib.sha512(authenticator_key.encode("utf8"))
        secret_hash = str(h.hexdigest())

        if secret_hash in self.user_authenticator_cache:
            user_mail = self.user_authenticator_cache[secret_hash]
            u = self.user.query.filter_by(email=user_mail).first()
            if u is not None and u.checkAuthenticator(authenticator_key) is True:
                return u
 
        all_user = self.user.query.all()
        for u in all_user:
            if u.checkAuthenticator(authenticator_key) is True:
                self.user_authenticator_cache[secret_hash] = u.email
                return u
        return None

    def checkUserAuthenticatorExists(self, authenticator_key):
        all_user = self.user.query.all()
        for u in all_user:
            if u.checkAuthenticator(authenticator_key) is True:
                return True
        return False

    def getUser(self, email):
        if email is None:
            return None
        return self.user.query.filter_by(email=email.strip().lower()).first()

    def checkUserExist(self, email):
        user = self.user.query.filter_by(email=email.strip().lower()).first()
        if user is None:
            return False
        else:
            return True

    def getUserRemainingPinAttempts(self, email):
        user = self.user.query.filter_by(email=email).first()
        remaining = self.pinAttemptLimit - user.failedPinAttempts
        if remaining > 0:
            return remaining
        else:
            return 0

    def checkUserPin(self, email, plaintext_pin):
        user = self.user.query.filter_by(email=email).first()
        if user.pinIsLocked is True:
            return False
        if user.checkPin(plaintext_pin) is True:
            user.failedPinAttempts = 0
            self.db.session.commit()
            return True
        else:
            user.failedPinAttempts = user.failedPinAttempts + 1
            if user.failedPinAttempts >= self.pinAttemptLimit:
                user.pinIsLocked = True
            self.db.session.commit()
            return False

    def checkUserPassword(self, username, password):
        pass
