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
from core.workspaces.models import PermissionGroup
from core.users.models import User
""" A view contaning a list of permission groups
"""


class PermissionUserList(DataView):

    uri = 'userList'
    requireLogin = True

    #    def __init__(self):
    #        super().__init__(name='PermissionList', uri ='permissionList')

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='ID', isKey=True)
        self.addStringProperty(name='name', label='Name')
        self.addStringProperty(name='email', label='eMail')
        self.addStringProperty(name='roles', label='Roles')
        self.addMultiSelectProperty(name='rolesSelection', label='Role keys', selectables=[])
        self.addBooleanProperty(name='admin', label='Admin')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for PermissionUserList")
        entrylist = []
        all_users = User.query.all()
        for u in all_users:

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = u.id
            entry.email = u.email
            entry.name = u.firstname + " " + u.lastname
            entry.admin = u.admin
            entry.roles = ""
            entry.rolesSelection = []
            if len(u.permission_groups) > 0:
                entry.roles = " : "
                for p in u.permission_groups:
                    entry.roles += p.name + " "
                    entry.rolesSelection.append(p.id)

            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        raise Exception("User creation not allowed in userList view")

    # Handler for a request to update a single view entry
    def removeViewEntryHandler(self, user, workspace, key):
        raise Exception("User removal not allowed in userList view")

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
        all_groups = PermissionGroup.query.all()
        u = User.query.filter_by(id=key).first()
        if hasattr(entry, 'rolesSelection'):
            u.permission_groups.clear()
            for g in all_groups:
                if g.id in entry['rolesSelection']:
                    u.permission_groups.append(g)
        self.emitSyncUpdate(key)
