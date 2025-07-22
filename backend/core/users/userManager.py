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
from core.common.checksum import crc16
from core.workspaces.workspaceHooks import WorkspaceHooks
from core.users.enum import (
    UserAuthenticatorStatus
)

class UserManager(object):
    """The UserManager ..."""

    def __init__(
        self,
    ):
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
        if self.checkUserExist(userdata["email"]):
            return None
        else:
            u = self.user(email=userdata["email"].strip().lower(), password=userdata["password"], isAdmin=False)
            if "firstname" in userdata:
                u.firstname = userdata["firstname"]
            if "lastname" in userdata:
                u.lastname = userdata["lastname"]
            if "organization" in userdata:
                u.organization = userdata["organization"]

            self.workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=u)
            self.db.session.add(u)
            self.db.session.commit()
            return u

    def updateUserPassword(self, user, newpassword):
        user.password = newpassword

    def updateAccessToken(self, username):
        session_expiration_minutes = self.config["SYSTEM"].get("session_expiration_minutes", 15)
        exp_delta = datetime.timedelta(minutes=session_expiration_minutes)
        access_token = create_access_token(identity=username, expires_delta=exp_delta)
        create_refresh_token(identity=username)
        return access_token

    def getAuthenticatorPublicKeyOrDefault(self, authenticator_private_key, authenticator_public_key):
        # for empty public keys use the default scenario to create one out of the private key
        if authenticator_public_key is None or authenticator_public_key == "":
            crc16_hash = crc16(bytearray(authenticator_private_key.encode()))
            key = "SERVER:CRC16:" + f"{crc16_hash:08X}"
            return key
        else:
            return "READER:" + authenticator_public_key

    def createUserAuthenticatorRequest(
        self,
        authenticator_private_key,
        authenticator_public_key,
        authenticator_type,
        validity_type,
        code_send_by,
        code_send_to,
        expire_days=3,
    ):
        token = secrets.token_hex(6)
        code = ":".join(a + b for a, b in zip(token[::2], token[1::2])).upper()
        a = self.authenticator_request()
        a.authenticator_type = authenticator_type
        a.validity_type = validity_type
        a.expire_date = arrow.utcnow().shift(days=expire_days)
        a.created_date = arrow.utcnow()
        a.code = code
        a.code_send_by = code_send_by
        a.code_send_to = code_send_to
        a.authenticator = authenticator_private_key
        a.authenticator_public_key = self.getAuthenticatorPublicKeyOrDefault(
            authenticator_private_key, authenticator_public_key
        )
        self.db.session.add(a)
        self.db.session.commit()
        return code

    def get_user_by_authenticator(self, authenticator_private_key, authenticator_public_key):
        # the hash are stored sha512-encrypted in the volatile cache (stored in the volatile memory / RAM)
        h = hashlib.sha512(authenticator_private_key.encode("utf8"))
        secret_hash = str(h.hexdigest())

        # check if the hash is in the volatile cache
        # the caching is add to even reduce the last bcrypt
        # the cache is stored in RAM and will be reset after app-restart
        if secret_hash in self.user_authenticator_cache:
            user_mail = self.user_authenticator_cache[secret_hash]
            u = self.user.query.filter_by(email=user_mail).first()
            logManager.info(f"Cashed secret hash {secret_hash:.10s}.. found, to get authenticator for : {str(u)}")
            if u is not None:
                if u.checkAuthenticator(authenticator_private_key) is True:
                    return u
                else:
                    logManager.warning(f"Failed to verify authenticator {secret_hash}. Going to remove from cache.")
                    del self.user_authenticator_cache[secret_hash]

        # get the public key from the private key. This will generate a public key
        # with a default algorithm (setuped) if needed.
        public_key = self.getAuthenticatorPublicKeyOrDefault(authenticator_private_key, authenticator_public_key)

        # get all users with the corresponding public key
        user_list = self.user.query.filter(self.user.authenticator_public_key == public_key).all()

        # if no user with the given public key found,
        # get all users with no or empty public key
        if len(user_list) == 0:
            user_list = self.user.query.filter(
                (self.user.authenticator_public_key == "") | (self.user.authenticator_public_key is None)
            ).all()
        else:
            logManager.info(f"Public key {public_key} found to preselect authenticators for users : {str(user_list)}")

        # iterate through the users list, contains one of the following:
        #  - a list of all users with the corresponding public key
        #  - (if not found) a list of all users without / empty public key
        for u in user_list:
            logManager.info(f"Check {authenticator_private_key} to match for user {str(u)}")

            if u.authenticator_status != UserAuthenticatorStatus.VALID:
                logManager.info(f"Skip user {str(u)} because authenticator status is not valid")
                continue
                
            # check the private key against the users authenticator
            if u.checkAuthenticator(authenticator_private_key) is True:
                # if found store the key in the volatile cache
                self.user_authenticator_cache[secret_hash] = u.email
                # if the public key is empty set a default public key out of the private key
                if u.authenticator_public_key == "" or u.authenticator_public_key is None:
                    u.authenticator_public_key = public_key
                return u
        # no user found for the given private key
        logManager.info(f"No user found for {str(authenticator_private_key)} and {str(authenticator_public_key)}")
        return None

    def checkUserAuthenticatorExists(self, authenticator_private_key, authenticator_public_key):
        user = self.get_user_by_authenticator(authenticator_private_key, authenticator_public_key)
        if user is None:
            return False
        else:
            return True

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
