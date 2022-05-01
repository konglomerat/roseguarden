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
from core.jobs import jobManager
from core.users.models import User
""" A view contaning a list of permissions
"""


class JobList(DataView):

    uri = 'jobList'
    requireLogin = True

    #    def __init__(self):
    #        super().__init__(name='PermissionList', uri ='permissionList')

    def defineProperties(self):
        self.addStringProperty(name='id', label='ID', isKey=True)
        self.addStringProperty(name='workspace', label='Workspace')
        self.addStringProperty(name='name', label='Name')
        self.addStringProperty(name='trigger', label='Triggered')
        self.addStringProperty(name='log', label='Log')
        self.addStringProperty(name='need_parameters', label='Parameters')
        self.addStringProperty(name='description', label='Description')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for JobList")
        entrylist = []
        all_jobs = jobManager.get_jobs()
        for key, j in all_jobs.items():

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = key
            entry.name = j.name
            entry.workspace = j.workspace
            entry.description = j.description
            entry.trigger = j.trigger

            if j.parameters is None:
                entry.need_parameters = "No"
            else:
                entry.need_parameters = "Yes"

            if j.log_in_db:
                entry.log = "Yes"
            else:
                entry.log = "No"

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
