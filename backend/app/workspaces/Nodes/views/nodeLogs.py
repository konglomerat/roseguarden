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
from core.nodes.models import NodeLog
from core.users.models import User
""" A view contaning a list of node logs
"""


class NodeLogs(DataView):

    uri = 'nodeLogs'
    requireLogin = True

    #    def __init__(self):
    #        super().__init__(name='PermissionList', uri ='permissionList')

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='ID', isKey=True)
        self.addStringProperty(name='date', label='Date')
        self.addStringProperty(name='node', label='Node')
        self.addStringProperty(name='node_actions', label='Node actions')
        self.addIntegerProperty(name='node_uptime', label='Node uptime [s]')
        self.addIntegerProperty(name='node_logcounter', label='Node logs')
        self.addIntegerProperty(name='node_errorcounter', label='Node errors')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for NodeLogs")
        entrylist = []
        all_logs = NodeLog.query.all()
        for lg in all_logs:

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = lg.id
            entry.node = lg.node_name + ' (' + lg.request_source + ')'
            entry.date = lg.request_date.format()
            entry.node_actions = lg.request_actions
            entry.node_uptime = lg.node_uptime
            entry.node_logcounter = lg.node_logcounter
            entry.node_errorcounter = lg.node_errorcounter

            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        pass

    # Handler for a request to update a single view entry
    def removeViewEntryHandler(self, user, workspace, key):
        pass

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        pass
