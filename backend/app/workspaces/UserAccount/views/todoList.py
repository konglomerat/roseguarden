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

from workspaces.UserAccount.models import Todo
""" A view contaning a list of all users not locked
"""


class TodoList(DataView):

    disable = True
    uri = 'todoList'
    requireLogin = True

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='ID', isKey=True)
        self.addStringProperty(name='description', label='Description')
        self.addSelectProperty(name='done', selectables=['Yes', 'No'], label='Done')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for UserView")
        userlist = []
        all_todos = Todo.query.all()
        for t in all_todos:
            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = t.id
            entry.description = t.description
            entry.done = 'Yes' if t.done else 'No'

            # append entry
            userlist.append(entry.extract())
        return userlist

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        t = Todo()
        t.description = "New todo"
        t.done = False
        workspace.db.session.add(t)
        self.emitSyncCreate(t.id, "todoList")
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        todo = Todo.query.filter_by(id=key).first()
        todo.description = entry.description
        self.emitSyncUpdate(key)
        print("Handle updateViewEntryHandler request for " + self.uri)
