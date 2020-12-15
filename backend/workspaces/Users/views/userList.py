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
__contact__ =  "roseguarden@fabba.space"
__credits__ = []
__license__ = "GPLv3"

from app.workspaces import DataView, Workspace
from app.users.models import User
from app import db

""" A view contaning a list of all users not locked
"""
class UserList(DataView):

    uri = 'userList'
    requireLogin = True

    def defineMetadata(self):
        self.addStringMeta("test")

    def defineProperties(self):            
        self.addMailProperty(name='email', label='eMail', isKey=True)
        self.addStringProperty(name='name', label='Name')
        self.addStringProperty(name='organization', label='Organization')
        self.addSelectProperty(name='verified', selectables=['Yes', 'No'], label='Verified')
        self.addActionProperty(name='lock', label='Lock user', action='lock', actionHandler=self.lockHandler, icon='clear') 
        self.addActionProperty(name='setAdmin', label='Give admin privileges', action='setAdmin', icon='flash_on', color="green") 
        self.addActionProperty(name='unsetAdmin', label='Remove admin privileges', action='unsetAdmin', icon='flash_off') 

    def getViewMetaHandler(self, user, workspace):
        meta = self.createMeta()
        meta.test = "Test"
        return meta

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for " +  self.uri)
        userlist = []
        all_user = User.query.filter_by(account_locked=False).all()
        for u in all_user:

            assert isinstance(u, User)
            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.email = u.email
            entry.name = "{0} {1}".format(u.firstname, u.lastname)
            entry.organization = u.organization
            entry.verified = 'Yes' if u.account_verified else 'No'

            # set entry actions
            entry.lock = False

            if user.admin is True and u.admin is False:
                entry.lock = True
                entry.setAdmin = True

            if user.admin is True and u.admin is True:
                entry.unsetAdmin = True

            userlist.append(entry.extract())
        return userlist

    def lockHandler(self, user, workspace, action, entrykey):
        locked_user = User.query.filter_by(email=entrykey).first()
        locked_user.account_locked = True
        self.emitSyncCreate(entrykey, "userLockedList")
        self.emitSyncRemove(entrykey, "userList")
        return {"a": 1}

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry 
    def createViewEntryHandler(self, user, workspace, entry):
        print("Handle createViewEntry request for " +  self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key,  entry):
        print("Handle updateViewEntryHandler request for " +  self.uri)


