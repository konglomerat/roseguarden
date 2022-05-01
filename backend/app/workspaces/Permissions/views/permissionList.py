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
from core.workspaces.models import Permission
from core.users.models import User
""" A view contaning a list of permissions
"""


class PermissionList(DataView):

    uri = 'permissionList'
    requireLogin = True

    #    def __init__(self):
    #        super().__init__(name='PermissionList', uri ='permissionList')

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='ID', isKey=True)
        self.addStringProperty(name='name', label='Name')
        self.addStringProperty(name='description', label='Description')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for PermissionList")
        entrylist = []
        all_permissions = Permission.query.all()
        for p in all_permissions:

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = p.id
            entry.name = p.name
            entry.description = p.description

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
