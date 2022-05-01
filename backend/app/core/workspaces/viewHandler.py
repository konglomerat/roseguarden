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

from core.actions.action import Action
from core.common.objDict import ObjDict
from core.logs import logManager
from core.actions import webclientActions
from core.actions.errors import RequireLoginError
import sys
import traceback


class RemoveViewEntryActionHandler(Action):
    def __init__(self, app, db, uri="removeViewEntry"):
        self.uri = uri
        self.app = app
        self.db = db
        # logManager.info("Instance of RemoveViewEntryActionHandler created")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute removal for view entry for", action['view'])
        viewname = action['view']

        if viewname in workspace.dataViews:
            view = workspace.dataViews[viewname]
            # check if login required for this view
            if view.requireLogin is True and user is None:
                raise RequireLoginError
            else:
                # build actions to get view
                responseActions = []
                try:
                    if view.entrykey not in action['entry']:
                        notification_action = webclientActions.NotificationAction.generate(
                            "UpdateViewEntryActionHandler miss entrykey", "error")
                        responseActions = [notification_action]
                    else:
                        view.dataSyncs = []
                        view.removeViewEntryHandler(user, workspace, action['entry'][str(view.entrykey)])
                        self.db.session.commit()
                        for v in view.dataSyncs:
                            updateView = workspace.dataViews[v['view']]
                            entries = updateView.getViewHandler(user, workspace, None)
                            meta_data = updateView.getViewMetaHandler(user, workspace)
                            properties = updateView.getProperties()
                            uri = workspace.uri + '/' + updateView.uri
                            loadviewaction = webclientActions.LoadViewAction.generate(
                                uri, properties, entries, meta_data)
                            responseActions.append(loadviewaction)
                    responseActions.append(
                        webclientActions.NotificationAction.generate("Removed successfully", "success"))
                    return 'success', responseActions
                except Exception as e:
                    notification_action = webclientActions.NotificationAction.generate(
                        "RemoveViewEntry '" + str(action['view']) + "' failed with: " + str(e), "error")
                    responseActions = [notification_action]
                    logManager.error(str(type(e).__name__) + 'in ExecuteViewActionsActionHandler ' + action['view'])
                    traceback.print_exc(file=sys.stdout)
                return 'success', responseActions

        notification_action = webclientActions.NotificationAction.generate("View >" + viewname + "< not found",
                                                                           "error")
        return 'success', [notification_action]


class CreateViewEntryActionHandler(Action):
    def __init__(self, app, db, uri="createViewEntry"):
        self.uri = uri
        self.app = app
        self.db = db
        # logManager.info("Instance of CreateViewEntryActionHandler created")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute creation of view entry for", action['view'])
        viewname = action['view']

        if viewname in workspace.dataViews:
            view = workspace.dataViews[viewname]
            # check if login required for this view
            if view.requireLogin is True and user is None:
                raise RequireLoginError
            else:
                # build actions to get view
                responseActions = []
                try:
                    view.dataSyncs = []
                    dictionary = action['entry']
                    view.createViewEntryHandler(user, workspace, ObjDict(dictionary))
                    self.db.session.commit()
                    for v in view.dataSyncs:
                        updateView = workspace.dataViews[v['view']]
                        entries = updateView.getViewHandler(user, workspace, None)
                        meta_data = updateView.getViewMetaHandler(user, workspace)
                        properties = updateView.getProperties()
                        uri = workspace.uri + '/' + updateView.uri
                        loadviewaction = webclientActions.LoadViewAction.generate(uri, properties, entries, meta_data)
                        responseActions.append(loadviewaction)
                    return 'success', responseActions
                except Exception as e:
                    notification_action = webclientActions.NotificationAction.generate(
                        "CreateViewEntry '" + str(action['view']) + "' failed with: " + str(e), "error")
                    responseActions = [notification_action]
                    logManager.error(str(type(e).__name__) + 'in ExecuteViewActionsActionHandler ' + action['view'])
                    traceback.print_exc(file=sys.stdout)
                return 'success', responseActions

        notification_action = webclientActions.NotificationAction.generate("View >" + viewname + "< not found",
                                                                           "error")
        return 'success', [notification_action]


class UpdateViewEntryActionHandler(Action):
    def __init__(self, app, db, uri="updateViewEntry"):
        self.uri = uri
        self.app = app
        self.db = db
        # logManager.info("Instance of UpdateViewEntryActionHandler created")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute update of view entry for '{}'", action['view'])
        viewname = action['view']

        if viewname in workspace.dataViews:
            view = workspace.dataViews[viewname]
            # check if login required for this view
            if view.requireLogin is True and user is None:
                raise RequireLoginError
            else:
                # build actions to get view
                responseActions = []
                try:
                    if view.entrykey not in action['entry']:
                        notification_action = webclientActions.NotificationAction.generate(
                            "UpdateViewEntryActionHandler miss entrykey", "error")
                        responseActions = [notification_action]
                    else:
                        view.dataSyncs = []
                        dictionary = action['entry']
                        view.updateViewEntryHandler(user, workspace, action['entry'][str(view.entrykey)],
                                                    ObjDict(dictionary))
                        self.db.session.commit()
                        for v in view.dataSyncs:
                            updateView = workspace.dataViews[v['view']]
                            entries = updateView.getViewHandler(user, workspace, None)
                            meta_data = updateView.getViewMetaHandler(user, workspace)
                            properties = updateView.getProperties()
                            uri = workspace.uri + '/' + updateView.uri
                            loadviewaction = webclientActions.LoadViewAction.generate(
                                uri, properties, entries, meta_data)
                            responseActions.append(loadviewaction)
                    responseActions.append(
                        webclientActions.NotificationAction.generate("Updated successfully", "success"))
                    return 'success', responseActions
                except Exception as e:
                    notification_action = webclientActions.NotificationAction.generate(
                        "UpdateViewEntry '" + str(action['view']) + "' failed with: " + str(e), "error")
                    responseActions = [notification_action]
                    logManager.error(str(type(e).__name__) + 'in ExecuteViewActionsActionHandler ' + action['view'])
                    traceback.print_exc(file=sys.stdout)
                return 'success', responseActions

        notification_action = webclientActions.NotificationAction.generate("View >" + viewname + "< not found",
                                                                           "error")
        return 'success', [notification_action]


class ExecuteViewActionsActionHandler(Action):
    def __init__(self, app, db, uri="executeViewAction"):
        self.uri = uri
        self.app = app
        self.db = db

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute action '{}' on view '{}'", action['viewAction'], action['view'])
        viewname = action['view']
        if viewname in workspace.dataViews:
            print('found view', viewname, 'in', workspace.name, workspace.dataViews[viewname])
            view = workspace.dataViews[viewname]

            # check if login required for this view
            if view.requireLogin is True and user is None:
                raise RequireLoginError
            else:
                # build actions to get view
                response_actions = []
                response_data = None
                try:
                    view.dataSyncs = []
                    dictionary = action
                    response_data = view.executeViewActionHandler(user, workspace, ObjDict(dictionary))
                    notification_action = webclientActions.NotificationAction.generate(
                        "Action '" + str(action['viewAction']) + "' executed", "info")
                    response_actions.append(notification_action)
                    self.db.session.commit()
                    for v in view.dataSyncs:
                        updateView = workspace.dataViews[v['view']]
                        meta_data = updateView.getViewMetaHandler(user, workspace)
                        entries = updateView.getViewHandler(user, workspace, None)
                        properties = updateView.getProperties()
                        uri = workspace.uri + '/' + updateView.uri
                        loadviewaction = webclientActions.LoadViewAction.generate(uri, properties, entries, meta_data)
                        response_actions.append(loadviewaction)

                except Exception as e:
                    notification_action = webclientActions.NotificationAction.generate(
                        "Action '" + str(action['viewAction']) + "' failed with: ", "error")
                    response_actions = [notification_action]
                    logManager.error(str(type(e).__name__) + 'in ExecuteViewActionsActionHandler', action['view'])
                    traceback.print_exc(file=sys.stdout)
                # entries = view.getViewHandler(user, workspace)
                # properties = view.getProperties()
                # uri = view.uri
                # loadviewaction = webclientActions.LoadViewAction.generate(uri, properties, entries)
                if response_data is not None:
                    return 'success', response_actions, response_data
                else:
                    return 'success', response_actions

        # view not found
        notification_action = webclientActions.NotificationAction.generate("View >" + viewname + "< not found",
                                                                           "error")
        return 'success', [notification_action]


class GetViewActionHandler(Action):
    def __init__(self, app, db, uri="getView"):
        self.uri = uri
        self.app = app
        self.db = db
        # logManager.info("Instance of GetViewActionHandler created")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute get view action for", action['view'])

        viewname = action['view']
        print(workspace.dataViews)
        if viewname in workspace.dataViews:
            print('found view', viewname, 'in', workspace.name, workspace.dataViews[viewname])
            view = workspace.dataViews[viewname]

            # check if login required for this view
            if view.requireLogin is True and user is None:
                raise RequireLoginError
            else:
                # build actions to get view
                meta_data = view.getViewMetaHandler(user, workspace)
                entries = view.getViewHandler(user, workspace, None)
                properties = view.getProperties()
                uri = workspace.uri + '/' + view.uri
                loadviewaction = webclientActions.LoadViewAction.generate(uri, properties, entries, meta_data)
                return 'success', [loadviewaction]

        # view not found
        notification_action = webclientActions.NotificationAction.generate("View >" + viewname + "< not found",
                                                                           "error")
        return 'success', [notification_action]
