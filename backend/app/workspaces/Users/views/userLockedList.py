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
from core.users import userManager
""" A view contaning a list of all users locked
"""


class UserLockedList(DataView):

    uri = 'userLockedList'
    requireLogin = True

    def defineProperties(self):
        self.addMailProperty(name='email', label='eMail', isKey=True)
        self.addStringProperty(name='name', label='Name')
        self.addActionProperty(name='unlock',
                               label='Unlock user',
                               action='unlock',
                               actionHandler=self.unlockHandler,
                               color='green',
                               icon='undo')
        self.addActionProperty(name='remove',
                               label='Remove user',
                               action='remove',
                               actionHandler=self.removeHandler,
                               icon='clear')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for UserView")
        userlist = []
        all_user = User.query.filter_by(account_locked=True).all()
        for u in all_user:
            assert isinstance(u, User)

            # get new empty entry
            entry = self.createEntry()

            # fill entry data
            entry.email = u.email
            entry.name = "{0} {1}".format(u.firstname, u.lastname)

            # set entry actions
            entry.remove = True
            entry.unlock = True
            userlist.append(entry.extract())
        return userlist

    def removeHandler(self, user, workspace, action, entrykey):
        userManager.removeUser(entrykey)
        self.emitSyncRemove(entrykey, "userLockedList")

    def unlockHandler(self, user, workspace, action, entrykey):
        locked_user = User.query.filter_by(email=entrykey).first()
        locked_user.account_locked = False
        self.emitSyncCreate(entrykey, "userList")
        self.emitSyncRemove(entrykey, "userLockedList")

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
