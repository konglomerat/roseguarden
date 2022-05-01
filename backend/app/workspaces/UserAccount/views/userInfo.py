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
from core.users.models import User
""" A View contaning the user info
"""


class UserInfo(DataView):

    uri = 'userInfo'
    requireLogin = True

    def defineProperties(self):
        self.addMailProperty(name='email', isKey=True)
        self.addStringProperty(name='firstname')
        self.addStringProperty(name='lastname')
        self.addStringProperty(name='organization')
        self.addStringProperty(name='phone')
        self.addStringProperty(name="pinIsLocked")
        self.addStringProperty(name="authenticator_status")
        self.addSelectProperty(name='verified', selectables=['Yes', 'No'], label='Verified')
        self.addDatetimeProperty(name="creationdate")
        self.addDatetimeProperty(name="lastlogindate")

    def getViewHandler(self, user: User, workspace: Workspace, query=None):

        userInfo = []
        # get new empty entry
        entry = self.createEntry()
        # fill entry
        entry.email = user.email
        entry.firstname = user.firstname
        entry.lastname = user.lastname
        entry.organization = user.organization
        entry.phone = user.phone
        entry.pinIsLocked = user.pinIsLocked
        entry.authenticator_status = user.authenticator_status.value
        entry.verified = 'Yes' if user.account_verified else 'No',
        entry.creationdate = user.account_created_date.format()
        entry.lastlogindate = user.last_login_date.format()
        # add single entry
        userInfo.append(entry.extract())
        return userInfo

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        if user.email != entry.email:
            raise Exception("Update denied")
        user.firstname = entry.firstname
        user.lastname = entry.lastname
        user.organization = entry.organization
        user.phone = entry.phone
        self.emitSyncUpdate(self.entrykey, 'userInfo')
        print("Handle updateViewEntryHandler request for " + self.uri)
