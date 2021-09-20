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

from core.workspaces.workspace import Workspace
from core.workspaces.dataView import DataView
from core.users.enum import UserAuthenticatorStatus
from core.users.models import User
from core.common.deface import deface_string_end
""" A view contaning a list of all user authenticator
"""


class AuthenticatorList(DataView):

    uri = 'userAuthenticatorList'
    requireLogin = True

    def defineProperties(self):
        self.addStringProperty(name='name', label='User name')
        self.addMailProperty(name='email', label='eMail', isKey=True)
        self.addStringProperty(name='status', label='User status')
        self.addBooleanProperty(name='verified', label='Verified', hide=True)
        self.addBooleanProperty(name='locked', label='Locked', hide=True)
        self.addStringProperty(name='auth_status', label='Auth. status')
        self.addStringProperty(name='hash', label='Auth. hash')
        self.addDatetimeProperty(name="change_date", label='Last change')
        self.addActionProperty(name='lock',
                               label='Lock auth.',
                               action='lock',
                               actionHandler=self.lockHandler,
                               icon='lock')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for " + self.uri)
        entrylist = []
        all_user = User.query.all()
        for u in all_user:

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.email = u.email
            entry.name = u.firstname + ' ' + u.lastname

            if u.authenticator is None or u.authenticator == "":
                entry.hash = "-"
            else:
                entry.hash = deface_string_end(u.authenticator.decode("utf-8"), 10)

            if u.authenticator_status == UserAuthenticatorStatus.VALID:
                entry.lock = True
            else:
                entry.lock = False

            entry.verified = u.account_verified
            entry.locked = u.account_locked
            if u.account_verified:
                entry.status = 'Verified'
                if u.account_locked:
                    entry.status = 'Verified and locked'
            else:
                entry.status = 'Not verified'
                if u.account_locked:
                    entry.status = 'Not verified and locked'

            entry.auth_status = str(u.authenticator_status.value)
            entry.change_date = u.authenticator_changed_date.format()

            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    def lockHandler(self, user, workspace, action, entrykey):
        user = User.query.filter_by(email=entrykey).first()
        user.authenticator_status = UserAuthenticatorStatus.LOCKED
        user.resetAuthenticator()
        self.emitSyncCreate(entrykey, "userAuthenticatorList")

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
