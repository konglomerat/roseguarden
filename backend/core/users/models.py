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

from core import db, bcrypt
from core.users.enum import AuthenticatorSendBy, AuthenticatorType, AuthenticatorValidityType, UserAuthenticatorStatus
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy_utils import ArrowType
import arrow


class User(db.Model):
    __tablename__ = 'users'
    # nonvolatile data stored in the db
    id = db.Column(db.Integer, primary_key=True)
    _authenticator_hash = db.Column(db.Binary(128))
    _password_hash = db.Column(db.Binary(128), nullable=False)
    _pin_hash = db.Column(db.Binary(128))
    _salt = db.Column(db.String(128))
    authenticator_public_key = db.Column(db.String(64), default="")
    authenticator_status = db.Column(db.Enum(UserAuthenticatorStatus), default=UserAuthenticatorStatus.UNSET)
    authenticator_changed_date = db.Column(ArrowType, default=arrow.utcnow)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String(64), default="")
    lastname = db.Column(db.String(64), default="")
    organization = db.Column(db.String(64), default="")
    phone = db.Column(db.String(64), default="")
    account_created_date = db.Column(ArrowType, default=arrow.utcnow)
    last_login_date = db.Column(ArrowType, default=arrow.utcnow)
    password_reset_expired_date = db.Column(ArrowType, default=arrow.utcnow)
    password_reset_hash = db.Column(db.String(128), default="")
    account_verified = db.Column(db.Boolean, default=False)
    account_locked = db.Column(db.Boolean, default=False)
    ldap = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    budget = db.Column(db.Float, default=0)
    pinIsLocked = db.Column(db.Boolean, default=False)
    failedPinAttempts = db.Column(db.Integer(), default=0)
    failedLoginAttempts = db.Column(db.Integer(), default=0)

    # def __init__(self, **kwargs):
    #    super(User, self).__init__(**kwargs)

    def __init__(self, email, password, isAdmin=False):
        self.email = email
        self.password = password
        self.admin = isAdmin

    def __repr__(self):
        return '<User {} {} : {}>'.format(self.firstname, self.lastname, self.email)

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def checkPassword(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    @hybrid_property
    def pin(self):
        return self._pin_hash

    @pin.setter
    def pin(self, plaintext_pin):
        self._pin_hash = bcrypt.generate_password_hash(plaintext_pin)

    @hybrid_method
    def checkPin(self, plaintext_pin):
        if self.pin is None or self.pin == "":
            return False
        else:
            return bcrypt.check_password_hash(self.pin, plaintext_pin)

    @hybrid_property
    def authenticator(self):
        return self._authenticator_hash

    @authenticator.setter
    def authenticator(self, plaintext_authenticator):
        self._authenticator_hash = bcrypt.generate_password_hash(plaintext_authenticator)

    @hybrid_method
    def resetAuthenticator(self):
        self._authenticator_hash = None

    @hybrid_method
    def setAuthenticatorHash(self, authenticator_hash):
        self._authenticator_hash = authenticator_hash

    @hybrid_method
    def checkAuthenticator(self, plaintext_authenticator):
        if self.authenticator is None or self.authenticator == "":
            return False
        else:
            return bcrypt.check_password_hash(self.authenticator, plaintext_authenticator)


class Authenticator(db.Model):
    __tablename__ = 'authenticator_requests'
    id = db.Column(db.Integer, primary_key=True)
    _authenticator_hash = db.Column(db.Binary(128))
    authenticator_public_key = db.Column(db.String(64), default="")
    authenticator_type = db.Column(db.Enum(AuthenticatorType), default=AuthenticatorType.USER)
    code = db.Column(db.String(128), default="")
    usage_limit = db.Column(db.Integer, default=1)
    validity_type = db.Column(db.Enum(AuthenticatorValidityType), default=AuthenticatorValidityType.ONCE)
    creation_date = db.Column(ArrowType, default=arrow.utcnow)
    expiration_date = db.Column(ArrowType, default=arrow.utcnow)
    code_send_by = db.Column(db.Enum(AuthenticatorSendBy), default=AuthenticatorSendBy.MAIL)
    code_send_to = db.Column(db.String(128), default="")

    @hybrid_property
    def authenticator(self):
        return self._authenticator_hash

    @authenticator.setter
    def authenticator(self, plaintext_authenticator):
        self._authenticator_hash = bcrypt.generate_password_hash(plaintext_authenticator)

    @hybrid_method
    def checkAuthenticator(self, plaintext_authenticator):
        return bcrypt.check_password_hash(self.authenticator, plaintext_authenticator)
