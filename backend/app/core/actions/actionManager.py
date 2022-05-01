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

from core import version
from core.logs import logManager
from core.common.objDict import ObjDict
from pprint import pprint
from core.actions.errors import NotFoundError, ExpiredError, RequireLoginError
from core.actions import webclientActions
import arrow
import random
import datetime
import string


class ActionManager(object):
    """ The ActionManager ...
    """
    def __init__(self, ):
        # preparation to instanciate
        self.actionsMap = {}

    def mapActions(self, app):
        logManager.info("")
        logManager.info("ActionManager map actions")

        # register workspaces
        for w in self.workspaceManager.workspaces:
            self.actionsMap[str(w.uri)] = {}
            # map actions for every workspace by there uri
            for a in w.actions:
                self.actionsMap[str(w.uri)][a.uri] = a

        pprint(self.actionsMap, indent=2)

    def mapWorkspaces(self, app):
        logManager.info("")
        logManager.info("ActionManager map workspaces")
        self.workspacesMap = {}
        for w in self.workspaceManager.workspaces:
            self.workspacesMap[str(w.uri)] = w

        pprint(self.workspacesMap, indent=2)

    def init_manager(self, app, db, userManager, menuBuilder, workspaceManager, nodeManager, config):
        self.app = app
        self.db = db
        self.config = config
        self.workspaceManager = workspaceManager
        self.userManager = userManager
        self.menuBuilder = menuBuilder
        self.nodeManager = nodeManager
        self.mapWorkspaces(app)
        self.mapActions(app)

        from core.actions.models import ActionLink
        self.actionLink = ActionLink

        logManager.info("ActionManager initialized")

    def createActionLink(self, workspace, action_uri, action_data_dict, redirect_to, once, need_login, expire_hours):
        al = self.actionLink()
        al.hash = ''.join(random.choices(string.ascii_letters + string.digits, k=96))
        al.workspace = workspace.uri
        al.action = action_uri
        al.expire_on_date = arrow.utcnow().shift(hours=expire_hours)
        al.action_data_json = action_data_dict
        al.run_only_once = once

        if redirect_to == "" or redirect_to is None:
            al.redirect_to = ""
        else:
            al.redirect_to = redirect_to

        al.need_login = need_login
        self.db.session.add(al)
        base_url = self.config['SYSTEM'].get('base_url', '')
        return '/'.join([base_url, 'actionlink', al.hash])

    def executeActionLink(self, hash, user):
        response_actions = []
        al = self.actionLink.query.filter_by(hash=hash).first()
        if al is None:
            raise NotFoundError
        if al.expire_on_date < arrow.utcnow():
            raise ExpiredError
        try:
            if str(al.workspace) in self.actionsMap:
                print('action workspace found')
                if al.action in self.actionsMap[al.workspace]:
                    print('action', al.action, 'found in workspace')
                    if user is None and al.need_login is True:
                        response_actions.append(
                            webclientActions.NotificationAction.generate("Login needed you will be redirected.",
                                                                         "success"))
                        response_actions.append(
                            webclientActions.RouteAction.generate("user/login?redirect=actionlink/" + hash, 3))
                        return response_actions
                    if al.redirect_to != "":
                        response_actions.append(webclientActions.RouteAction.generate(al.redirect_to, 2))
                    workspace = self.workspacesMap[al.workspace]
                    print(user, workspace)
                    param = al.action_data_json
                    state, actions = self.actionsMap[al.workspace][al.action].handle(
                        ObjDict(param), user, workspace, self)
                    if state == 'success':
                        logManager.info('Actionlink succed with {} for user: {}', actions, user)
                    else:
                        logManager.error('Actionlink failed with {} for user: {}', actions, user)
                        raise Exception(str('Action failed with {} for user: {}', actions, user))
                    response_actions = response_actions + actions
                    return response_actions
                else:
                    logManager.error('action ' + al.action + ' not found in ' + al.workspace)
                    raise Exception(str('action workspace: "' + al.workspace + '" not found'))
            else:
                logManager.error('action workspace: "' + al.workspace + '"not found')
                raise Exception(str('action workspace: "' + al.workspace + '"not found'))

        except Exception as e:
            raise e
        finally:
            if al.run_only_once is True:
                self.db.session.delete(al)

    def createDataViewActionLink(self, entrykey, workspace, data_view_uri, action_property, action=None):
        raise NotImplementedError

    def buildActionReply(self, actions, response={}):
        reply = {}
        reply['head'] = {}
        reply['head']['version'] = version
        reply['actions'] = actions
        reply['response'] = response
        return reply

    def handleActionRequest(self, identity, expire_date, request):
        actions = request['actions']
        response_actions = []
        response_data = {}
        user = None
        print('identity = ', identity)
        for action in actions:
            if action['workspace'] in self.actionsMap:
                print('action workspace found')
                if action['action'] in self.actionsMap[action['workspace']]:
                    print('action', action['action'], 'found in workspace')
                    user = (self.userManager.getUser(identity))
                    workspace = self.workspacesMap[action['workspace']]
                    try:
                        handle_result = self.actionsMap[action['workspace']][action['action']].handle(
                            ObjDict(action), user, workspace, self)
                    except RequireLoginError:
                        route_action = webclientActions.RouteAction.generate('dashboard', delay=0)
                        notification_action = webclientActions.NotificationAction.generate("Login required",
                                                                                           "error",
                                                                                           delay=2)
                        response_actions = [route_action, notification_action]
                        return self.buildActionReply(response_actions, response_data)

                    handle_result_len = len(handle_result)

                    if handle_result_len == 1:
                        state, actions, response = handle_result, [], {}
                    elif handle_result_len == 2:
                        state, actions, response = handle_result[0], handle_result[1], {}
                    elif handle_result_len == 3:
                        state, actions, response = handle_result
                    else:
                        state, actions, response = "error", [], {}

                    self.db.session.commit()
                    if state == 'success':
                        pass
                    else:
                        logManager.error('Action {} failed', action['action'])

                    response_intersection = response_data.keys() & response
                    if len(response_intersection) != 0:
                        logManager.warning('Action response data for {} overrided the following properties',
                                           action['action'], response_intersection)
                    response_data = {**response_data, **response}
                    response_actions = response_actions + actions

                else:
                    logManager.error('action ' + action['action'] + ' not found in ' + action['workspace'])
            else:
                logManager.error('action workspace: "' + action['workspace'] + ' "not found')

        if expire_date is not None and identity is not None:
            difference = expire_date - datetime.datetime.now()
            remaining_minutes = difference.seconds / 60
            session_expiration_minutes = self.config['SYSTEM'].get('session_expiration_minutes', 15)
            if remaining_minutes < session_expiration_minutes * 0.5:
                access_token = self.userManager.updateAccessToken(identity)
                response_actions.insert(0, webclientActions.UpdateSessionTokenAction.generate(access_token))

        return self.buildActionReply(response_actions, response_data)
