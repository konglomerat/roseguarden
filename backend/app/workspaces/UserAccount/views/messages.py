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
from core.messages.models import Message
""" A view contaning a list of all users not locked
"""


class UserMessages(DataView):

    uri = 'userMessages'
    requireLogin = True

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='ID', isKey=True)
        self.addStringProperty(name='subject', label='Subject')
        self.addStringProperty(name='sender', label='Subject')
        self.addDatetimeProperty(name='datetime', label='Date')
        self.addBooleanProperty(name='read', label='Read')
        self.addActionProperty(name='getMesasge',
                               label='Get message',
                               action='getMesasge',
                               actionHandler=self.getMesasge,
                               icon='clear')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for UserView")
        messages_list = []
        messages_all = Message.query.filter_by(recipient_email=user.email).all()
        for m in messages_all:
            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = m.id
            entry.subject = m.subject
            entry.datetime = m.message_send_date.format('YYYY-MM-DD HH:mm:ss')
            entry.sender = m.sender_name
            entry.read = m.message_read

            # append entry
            messages_list.append(entry.extract())
        return messages_list

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    def getMesasge(self, user, workspace, action, entrykey):
        msg = Message.query.filter_by(id=entrykey).first()
        msg.message_read = True
        if msg is not None:
            return {"message": msg.message_html}
        else:
            return {"message": "Not found"}

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        # t = Todo()
        # t.description = "New todo"
        # t.done = False
        # workspace.db.session.add(t)
        # self.emitSyncCreate(t.id, "todoList")
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        # todo = Todo.query.filter_by(id=key).first()
        # todo.description = entry.description
        # self.emitSyncUpdate(key)
        print("Handle updateViewEntryHandler request for " + self.uri)
