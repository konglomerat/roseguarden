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
import arrow
import hashlib

from core.logs import logManager
from core.nodes import nodeclientActions
from core.nodes.errors import AuthorizationError


class NodeManager(object):
    """ The NodeManager holds all available node-types and load them while creation.
    """
    def __init__(self):
        self.node_classes = {}
        self.nodes = {}

    def disable_node(self, node):
        try:
            del self.nodes[node.fingerprint]
        except KeyError:
            logManager.warning("Failed to disable node.")

        node.active = False
        node.status = "Disabled"

    def activate_node(self, node):
        logManager.info("Activate node " + node.name)
        nodeInstance = None
        for k, v in self.node_classes.items():
            if v.class_id == node.class_id:
                nodeInstance = self.node_classes[k]()
                nodeInstance.identity = node.identification

        if nodeInstance is not None:
            self.nodes[node.fingerprint] = nodeInstance
        else:
            logManager.error("NodeManager is unable to register node {} [{}] with unknown class_id '{}'".format(
                node.name, node.fingerprint, node.class_id))

        node.active = True
        node.status = "Active"

    def register_node_class(self, workspace, node_class):
        nodeInstance = node_class()
        nodekey = str(workspace.name) + '/' + nodeInstance.name
        self.node_classes[nodekey] = node_class

    def init_nodes(self):
        logManager.info('Initialize nodes')
        all_nodes = self.node.query.all()
        for n in all_nodes:
            if n.authorized is True:
                self.activate_node(n)
        self.db.session.commit()

    def get_node(self, fingerprint):
        if fingerprint in self.nodes:
            return self.nodes[fingerprint]
        else:
            return None

    def get_node_classes(self):
        return self.node_classes

    def buildActionReply(self, actions, target="node", source="server", version="1.0.0"):
        reply = {}
        reply['header'] = {}
        reply['header']['version'] = version
        reply['header']['target'] = target
        reply['header']['source'] = source
        reply['actions'] = actions
        return reply

    def revoke_node_authorization(self, node):
        node.authorized = False
        node.authorization_status = "Revoked"
        self.db.session.commit()

        self.disable_node(node)

    def authorizeNode(self, node_fingerprint, commit=True):
        n = self.node.query.filter_by(fingerprint=node_fingerprint).first()
        if n is not None:
            n.authorized = True
            n.authorization_status = "Ok"
            self.activate_node(n)
            if commit is True:
                self.db.session.commit()

    def handle_authorization_request(self, node, authentification_plain):
        node_class_key = None
        for key, value in self.node_classes.items():
            if value.class_id == node.class_id:
                if node_class_key is None:
                    node_class_key = key
                else:
                    raise AuthorizationError("Authorization failed, duplicate class_id for "
                                             + self.node_classes[key].name + " and "
                                             + self.node_classes[node_class_key].name)

        if node_class_key is None:
            raise AuthorizationError("Authorization failed, no match found for registered node classes with class_id: "
                                     + node.class_id)

        if node.checkAuthentification(authentification_plain) is False:
            raise AuthorizationError("Authorization failed, authentification secret mismatch.")

        node.authorized = True
        node.authorization_status = "Ok"

        self.activate_node(node)

        self.db.session.commit()

    def create_node_from_identification(self, ident_action, fingerprint, authentification_plain):
        # make copy of the ident action and remove action specific entries
        ident_copy = ident_action.copy()
        if 'version' in ident_copy:
            del ident_copy['version']
        if 'action' in ident_copy:
            del ident_copy['action']
        if 'actionid' in ident_copy:
            del ident_copy['actionid']

        # create a sha256 hash
        ident_hash = hashlib.sha256()
        ident_copy_json_encoded = json.dumps(ident_copy, sort_keys=True).encode()
        ident_hash.update(ident_copy_json_encoded)

        # create node
        name = ident_action['nodename']
        n = self.node(name, fingerprint, authentification_plain)
        n.name = ident_action['nodename']
        n.fingerprint = fingerprint
        n.authentification = authentification_plain
        n.class_name = ident_action['classname']
        n.class_id = ident_action['classid']
        n.class_workspace = ident_action['classworkspace']
        n.identification = ident_copy
        n.identification_hash = ident_hash.hexdigest()

        self.db.session.add(n)
        self.db.session.commit()

    def check_for_identification_sync(self, request_actions):
        for i in request_actions:
            if i['action'] == "syncNodeIdentification":
                return i
        return None

    def handle_node_request(self, request):
        logManager.info('Handle node action request')
        header = request['header']
        source = header['source']
        fingerprint = header['fingerprint']
        authentification = header['authentification']
        actions = request['actions']

        actions_string = ""
        action_names_list = []
        if len(actions) > 0:
            for i in actions:
                action_names_list.append(i['action'])
                if actions_string != "":
                    actions_string = actions_string + ", "
                actions_string = actions_string + i['action']

        # create node log
        lg = self.nodeLog()
        lg.request_source = header['source']
        lg.node_uptime = header['uptime']
        lg.node_logcounter = header['logcounter']
        lg.node_errorcounter = header['errorcounter']
        lg.request_actions = actions_string
        lg.request_date = arrow.utcnow()
        self.db.session.add(lg)
        self.db.session.commit()

        # check
        n = self.node.query.filter_by(fingerprint=fingerprint).first()
        if n is None:
            logManager.info("request of unknown node {} ({})".format(source, fingerprint))
            ident_action = self.check_for_identification_sync(actions)
            if ident_action is not None:
                self.create_node_from_identification(ident_action, fingerprint, authentification)
            else:
                syncIdentAction = nodeclientActions.SendIdentificationAction.generate()
                return self.buildActionReply([syncIdentAction])

        if n is not None:
            n.last_request_on = arrow.utcnow()
            self.db.session.commit()

        if n.authorized is False:
            raise AuthorizationError("Node is not authorized.")

        if n.active is False or fingerprint not in self.nodes:
            raise AuthorizationError("Node is not active and can't handle requests.")

        self.nodes[fingerprint].check_actions_available(action_names_list)

        reply_actions = []
        for a in actions:
            action_reply = self.nodes[fingerprint].handleNodeActionRequest(n, a, header)
            reply_actions = reply_actions + action_reply
        self.db.session.commit()

        # node is known
        logManager.info("handle request of {} ({})".format(source, fingerprint))
        return self.buildActionReply(reply_actions)

    def init_manager(self, app, db, workspaceManager):
        self.app = app
        self.db = db
        self.workspaceManager = workspaceManager
        logManager.info("NodeManager initialized")

        from core.nodes.models import Node, NodeLog
        self.node = Node
        self.nodeLog = NodeLog
