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

import json
from core.workspaces.workspace import Workspace
from core.workspaces.dataView import DataView
from core.users.models import User
from core.nodes.models import Node
from core.nodes.errors import AuthorizationError
from core.nodes import nodeManager
""" A view contaning a list of permission groups
"""


class NodeList(DataView):

    uri = 'nodeList'
    requireLogin = True

    def defineProperties(self):
        self.addIntegerProperty(name='id', label='ID', isKey=True, hide=True)
        self.addStringProperty(name='name', label='Name')
        self.addBooleanProperty(name='active', label='Active', hide=True)
        self.addStringProperty(name='status', label='Status')
        self.addBooleanProperty(name='authorized', label='Authorized', hide=True)
        self.addStringProperty(name='authorization_status', label='Authorization')
        self.addStringProperty(name='fingerprint', label='Fingerprint')
        self.addStringProperty(name='nodeclass', label='Class id')
        self.addStringProperty(name='workspace', label='Workspace')
        self.addDateProperty(name='last_request_datetime', label='Last request')
        self.addActionProperty(name='revoke',
                               label='Revoke',
                               action='revoke',
                               actionHandler=self.revoke,
                               color="orange",
                               icon='block')
        self.addActionProperty(name='remove',
                               label='Remove',
                               action='remove',
                               actionHandler=self.removeViewEntryHandler,
                               icon='clear')
        self.addActionProperty(name='requestAuthorization',
                               label='',
                               action='requestAuthorization',
                               actionHandler=self.requestAuthorization,
                               icon='')
        self.addActionProperty(name='getIdentification',
                               label='',
                               action='getIdentification',
                               actionHandler=self.getIdentification,
                               icon='')

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for NodeList")
        entrylist = []
        all_nodes = Node.query.all()
        for n in all_nodes:

            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = n.id
            entry.name = n.name
            entry.nodeclass = n.class_id
            entry.fingerprint = n.fingerprint
            entry.authorized = n.authorized
            entry.workspace = n.class_workspace
            entry.authorization_status = n.authorization_status
            entry.active = n.active
            entry.status = n.status
            entry.last_request_datetime = n.last_request_on.format()
            if user.admin is True:
                entry.remove = True
                if entry.authorized is True:
                    entry.revoke = True
            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name, len(self.properties))

    def getSettings(self, user, workspace, action, entrykey):
        pass

    def revoke(self, user, workspace, action, entrykey):
        n = Node.query.filter_by(id=entrykey).first()
        nodeManager.revoke_node_authorization(n)
        self.emitSyncUpdate(entrykey)

    def requestAuthorization(self, user, workspace, action, entrykey):
        n = Node.query.filter_by(id=entrykey).first()
        try:
            nodeManager.handle_authorization_request(n, action['entry']['authentification'])
        except AuthorizationError as e:
            return {'succeed': False, 'message': str(e)}

        self.emitSyncUpdate(entrykey)
        return {'succeed': True, 'message': "Authorization successful"}

    def getIdentification(self, user, workspace, action, entrykey):
        ident_json = {}
        n = Node.query.filter_by(id=entrykey).first()
        ident_json['fingerprint'] = n.fingerprint
        ident_json['classid'] = n.class_id
        ident_json['workspace'] = n.class_workspace
        ident_json['identification'] = json.dumps(n.identification, indent=1)
        return ident_json

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        pass

    # Handler for a request to update a single view entry
    def removeViewEntryHandler(self, user, workspace, entrykey):
        print("Handle removeViewEntryHandler request for " + self.uri)
        n = Node.query.filter_by(id=entrykey).first()
        workspace.db.session.delete(n)
        self.emitSyncRemove(entrykey)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        pass
