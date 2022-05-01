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
from core.nodes.models import Node
from workspaces.Access.models import SpaceAccessSpace
from core.users.models import User
""" A view contaning a list of spaces
"""


class SpacesList(DataView):

    uri = 'spacesList'
    requireLogin = True

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='ID', isKey=True)
        self.addStringProperty(name='name', label='Name')
        self.addStringProperty(name='description', label='Description')
        self.addMultiSelectProperty(name='entrance_nodes', label='Entrance node keys', selectables=[])

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for SpacesList")
        entrylist = []
        all_spaces = SpaceAccessSpace.query.all()
        for s in all_spaces:

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = s.id
            entry.name = s.name
            entry.description = s.description
            entry.entrance_nodes = []
            for si in s.entrance_nodes:
                entry.entrance_nodes.append(si.id)

            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        s = SpaceAccessSpace()
        if hasattr(entry, 'name'):
            s.name = entry.name
        else:
            s.name = "New space"
        self.emitSyncCreate(s.id, "spacesList")
        workspace.db.session.add(s)
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def removeViewEntryHandler(self, user, workspace, key):
        print("Handle removeViewEntryHandler request for " + self.uri)
        s = SpaceAccessSpace.query.filter_by(id=key).first()
        workspace.db.session.delete(s)
        self.emitSyncRemove(key)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
        all_nodes = Node.query.all()
        s = SpaceAccessSpace.query.filter_by(id=key).first()
        if hasattr(entry, 'name'):
            s.name = entry.name
        if hasattr(entry, 'description'):
            s.description = entry.description
        if hasattr(entry, 'entrance_nodes'):
            s.entrance_nodes.clear()
            for n in all_nodes:
                if n.id in entry['entrance_nodes']:
                    s.entrance_nodes.append(n)
        self.emitSyncUpdate(key)
