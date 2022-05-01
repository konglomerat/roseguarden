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
from core.users.enum import AuthenticatorValidityType
from core.common.deface import deface_string_end, deface_string_middle
from core.users.models import Authenticator, User
""" A view contaning a list of all available authenticator
"""


class AuthenticatorList(DataView):

    uri = 'authenticatorList'
    requireLogin = True

    def defineMetadata(self):
        self.addStringMeta("test")

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='Id', isKey=True, hide=True)
        self.addStringProperty(name='type', label='Type')
        self.addStringProperty(name='hash', label='Hash')
        self.addStringProperty(name='code', label='Code')
        self.addDatetimeProperty(name="code_send", label='Code send')
        self.addDatetimeProperty(name="creation_date", label='Created at')
        self.addStringProperty(name='validity', label='Validity')
        self.addDatetimeProperty(name="expiration_date", label='Expires at')

    def getViewMetaHandler(self, user, workspace):
        meta = self.createMeta()
        meta.test = "Test"
        return meta

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for AuthenticatorRequestList")

        entrylist = []
        all_authenticators = Authenticator.query.all()
        for ar in all_authenticators:

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = ar.id
            entry.type = str(ar.authenticator_type.value)
            entry.hash = deface_string_end(ar.authenticator.decode("utf-8"), 10)

            entry.code = deface_string_middle(ar.code, 4)

            if ar.validity_type == AuthenticatorValidityType.ONCE:
                entry.validity = "Once"
            if ar.validity_type == AuthenticatorValidityType.EXPIRATION_DATE:
                entry.validity = "Expires"
            if ar.validity_type == AuthenticatorValidityType.LIMITED_USAGE:
                entry.validity = str(ar.usage_limit) + " times"
            entry.code_send = str(ar.code_send_by.value) + ' (' + str(ar.code_send_to) + ')'
            entry.creation_date = ar.creation_date.format()
            entry.expiration_date = ar.expiration_date.format()

            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
