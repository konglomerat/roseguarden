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

import inspect
import sys
import traceback
import os
import pkgutil
from core.workspaces.workspace import Workspace
from core.workspaces.commands import roseguarden_cli
from core.workspaces.workspaceHooks import WorkspaceHooks
from core.logs import logManager


class WorkspaceManager(object):
    """ The WorkspaceManager holds all available workspaces and load them while creation.
    """
    def __init__(self, workspaceSource):
        self.workspaceSource = workspaceSource

    def init_app(self, app, db):
        self.app = app
        self.db = db
        with self.app.app_context():
            self.reloadWorkspaces()
            self.registerWorkspacePlugins()
            self.registerWorkspacePermissions()
            logManager.info("Workspaces initialized")
            self.register_command_line_client()
            logManager.info("Command line client initialized")

    def getWorkspace(self, name):
        for w in self.workspaces:
            if w.name is name:
                return w
        return None

    def triggerWorkspaceHooks(self, hook: WorkspaceHooks, **kwargs):
        for w in self.workspaces:
            try:
                if hook == WorkspaceHooks.CREATEUSER:
                    w.createUserHook(**kwargs)
                if hook == WorkspaceHooks.REMOVEUSER:
                    w.removeUserHook(**kwargs)
            except Exception as e:
                logManager.error('Failed to run hook {} on {} with {}'.format(hook, w.name, e))

    def reloadWorkspaces(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.workspaces = []
        self.seen_paths = []
        logManager.info("")
        logManager.info(f'Discover workspaces in path : {self.workspaceSource}')
        self.discoverWorkspaces(self.workspaceSource)

    def registerWorkspacePermissions(self):
        """ Run createPermissions for all workspaces and store permissions
        """
        logManager.info("")
        all_permissions = {}
        for ws in self.workspaces:

            workspace_permissions = ws.permissions
            if workspace_permissions is not None:
                all_permissions = {**all_permissions, **workspace_permissions}
            logManager.info(f'Register permissions for {ws.name}-workspace : {workspace_permissions}')

        logManager.info(f'Delete orphaned permissions for {ws.name}-workspace')

        # delete orphaned permissions for security reasons
        from .models import Permission
        from core import db
        engine = db.get_engine()
        table_exists = engine.dialect.has_table(engine, Permission.__tablename__)
        if table_exists:
            db_permissions = Permission.query.all()
            for permission in db_permissions:
                if permission.name not in all_permissions:
                    print("Delete orphaned permission: ", permission)
                    self.db.session.delete(permission)
                    self.db.session.commit()

    def register_command_line_client(self):
        self.app.cli.add_command(roseguarden_cli)

    def registerWorkspacePlugins(self):
        """Recursively walk the supplied package to retrieve components for all plugins (workspaces)
        """
        logManager.info("")
        logManager.info("Register components from workspaces:")
        logManager.info("")

        for w in self.workspaces:
            logManager.info(f'Workspace: "{w.name}"')

            # try to discover commands
            try:
                w.discoverCommands(self.workspaceSource)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(f'Workspace "{w.name}" unable to discover commands  ({str(type(e).__name__)}:{e})')

            # try to register permissions
            try:
                w.discoverPermissions(self.workspaceSource)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(f'Workspace "{w.name}" unable to discover permissions  ({str(type(e).__name__)}:{e})')

            # try to register dataViews
            try:
                w.discoverDataViews(self.workspaceSource)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(f'Workspace "{w.name}" unable to discover dataviews  ({str(type(e).__name__)}:{e})')

            # try to register jobs
            try:
                w.discoverJobs(self.workspaceSource)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(f'Workspace "{w.name}" unable to discover jobs  ({str(type(e).__name__)}:{e})')

            # try to register actions
            try:
                w.discoverActions(self.workspaceSource)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(f'Workspace "{w.name}" unable to discover actions  ({str(type(e).__name__)}:{e})')

            # try to register sections
            try:
                w.discoverSections(self.workspaceSource)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(f'Workspace "{w.name}" unable to discover sections  ({str(type(e).__name__)}:{e})')

            # try to register node classes
            try:
                w.discoverNodeClasses(self.workspaceSource)
            except ModuleNotFoundError:
                logManager.info(f'No node classes discovered for "{w.name}"')
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(
                    f'Workspace "{w.name}" unable to discover node classes  ({str(type(e).__name__)}:{e})')

            # try to register permissions
            try:
                w.discoverPages(self.workspaceSource)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                logManager.error(f'Workspace "{w.name}" unable to discover pages  ({str(type(e).__name__)}:{e})')

            logManager.info("")

    def discoverModels(self):
        source = self.workspaceSource
        imported_source = __import__(source, fromlist=['blah'])
        all_current_paths = []

        # all_current_paths.append(imported_source.__path__._path)

        if isinstance(imported_source.__path__, str):
            all_current_paths.append(imported_source.__path__)
        else:
            all_current_paths.extend([x for x in imported_source.__path__])

        # remove duplicates
        all_current_paths = list(set(all_current_paths))

        for pkg_path in all_current_paths:
            # Walk through all sub directories
            child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

            for child_pkg in child_pkgs:
                try:
                    __import__(source + '.' + child_pkg + '.models', fromlist=['blah'])
                except ModuleNotFoundError:
                    modelmodule = source + '.' + child_pkg + '.models'
                    logManager.info(f'No model found for {modelmodule}')
                print(child_pkg)
        print("Finished")

    def discoverWorkspaces(self, source):
        """Recursively walk the supplied package to retrieve all plugins (workspaces)
        """
        imported_source = __import__(source, fromlist=['blah'])
        all_current_paths = []

        # all_current_paths.append(imported_source.__path__._path)

        if isinstance(imported_source.__path__, str):
            all_current_paths.append(imported_source.__path__)
        else:
            all_current_paths.extend([x for x in imported_source.__path__])

        # remove duplicates
        all_current_paths = list(set(all_current_paths))

        for pkg_path in all_current_paths:
            # Walk through all sub directories
            child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

            # Every sub directory contains one workspace
            for child_pkg in child_pkgs:
                imported_package = __import__(source + '.' + child_pkg, fromlist=['blah'])
                for _, workspacename, ispkg in pkgutil.iter_modules(imported_package.__path__,
                                                                    imported_package.__name__ + '.'):
                    workspaceCounter = 0
                    if not ispkg:
                        workspace_module = __import__(workspacename, fromlist=['blah'])
                        clsmembers = inspect.getmembers(workspace_module, inspect.isclass)

                        for (_, c) in clsmembers:
                            # Check for workspace classes
                            if issubclass(c, Workspace) & (c is not Workspace):
                                workspaceCounter += 1
                                if workspaceCounter > 1:
                                    logManager.error(
                                        'Only one workspace is allowed for one folder, other workspaces will skipped')
                                    break

                                uri = ""
                                if hasattr(c, 'uri'):
                                    uri = c.uri
                                else:
                                    logManager.error(
                                        f'No uri defined and will not be accessable for workspace: {c.__module__}')

                                name = c.__name__
                                if hasattr(c, 'name'):
                                    name = c.name
                                workspaceInstance = c(self.app, self.db, name, uri)
                                workspaceInstance.path = os.path.dirname(workspace_module.__file__)
                                logManager.info('Workspace discovered : {} [{}] with uri "{}"'.format(
                                    workspaceInstance.name, c.__module__, workspaceInstance.uri))
                                if workspaceInstance.disable is True:
                                    logManager.info('Workspace {} [{}] is disabled and wont show up.'.format(
                                        workspaceInstance.name, c.__module__))
                                else:
                                    self.workspaces.append(workspaceInstance)
