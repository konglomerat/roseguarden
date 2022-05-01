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

import copy
from core.common.objDict import ObjDict


class DataView(object):
    """Build up data-views
    """
    disable = False
    requireLogin = True
    requirePermission = None  # a permission is required in the meaning of one of the following

    def __init__(self, name=None, uri=None):
        self.description = 'UNKNOWN'
        if name is None:
            self.name = type(self).__name__
        else:
            self.name = name
        if uri is None:
            self.uri = self.name
        else:
            self.uri = uri
        self.requireLogin = True
        self.properties = []
        self.metadata = []
        self.dataAction = {}
        self.dataUpdateHandler = {}
        self.dataUpdates = []
        self.dataSyncs = []
        self.entrykey = None
        self.entrytype = None
        self.entryPropList = {}
        self.metaDataList = {}

    def createMeta(self):
        return ObjDict(self.metaDataList.copy())

    def addMailMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'email'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def addStringMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'string'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def addIntegerMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'integer'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def addDoubleMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'double'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def addBooleanMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'boolean'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def addTimeMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'time'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def addDateMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'date'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def addDatetimeMeta(self, name, label="", group=None, description=""):
        meta = {'name': name, 'label': label, 'type': 'datetime'}
        self.metaDataList[name] = None
        self.metadata.append(meta)

    def createEntry(self):
        return ObjDict(self.entryPropList.copy())

    def getProperties(self):
        properties = []
        for p in self.properties:
            pn = copy.copy(p)
            if pn['type'] == 'multiselect' or pn['type'] == 'select':
                try:
                    if callable(p['selection']):
                        pn['selection'] = p['selection']()
                    else:
                        pn['selection'] = p['selection']
                except Exception as e:
                    raise e
            properties.append(pn)
        return properties

    def addMailProperty(self,
                        name,
                        label="",
                        group=None,
                        updateHandler=None,
                        isKey=False,
                        readOnly=True,
                        description=""):
        prop = {'name': name, 'label': label, 'type': 'email'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name

        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addStringProperty(self,
                          name,
                          label="",
                          group=None,
                          updateHandler=None,
                          isKey=False,
                          readOnly=True,
                          description="",
                          hide=False):
        prop = {'name': name, 'label': label, 'type': 'string'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['hide'] = hide
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addDoubleProperty(self,
                          name,
                          label="",
                          group=None,
                          updateHandler=None,
                          isKey=False,
                          readOnly=True,
                          description=""):
        prop = {'name': name, 'label': label, 'type': 'double'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addIntegerProperty(self,
                           name,
                           label="",
                           group=None,
                           updateHandler=None,
                           isKey=False,
                           readOnly=True,
                           description="",
                           hide=False):
        prop = {'name': name, 'label': label, 'type': 'integer'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['hide'] = hide
        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addDatetimeProperty(self,
                            name,
                            label="",
                            group=None,
                            updateHandler=None,
                            isKey=False,
                            readOnly=True,
                            description=""):
        prop = {'name': name, 'label': label, 'type': 'datetime'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addTimeProperty(self,
                        name,
                        label="",
                        group=None,
                        updateHandler=None,
                        isKey=False,
                        readOnly=True,
                        description=""):
        prop = {'name': name, 'label': label, 'type': 'time'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addDateProperty(self,
                        name,
                        label="",
                        group=None,
                        updateHandler=None,
                        isKey=False,
                        readOnly=True,
                        description=""):
        prop = {'name': name, 'label': label, 'type': 'date'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addBooleanProperty(self,
                           name,
                           label="",
                           group=None,
                           updateHandler=None,
                           isKey=False,
                           readOnly=True,
                           description="",
                           hide=False):
        prop = {'name': name, 'label': label, 'type': 'boolean'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['group'] = group
        prop['hide'] = hide
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addSelectProperty(self,
                          name,
                          selectables,
                          label="",
                          group=None,
                          updateHandler=None,
                          isKey=False,
                          readOnly=True,
                          description=""):
        prop = {'name': name, 'label': label, 'type': 'select'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['selection'] = selectables
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addMultiSelectProperty(self,
                               name,
                               selectables,
                               label="",
                               group=None,
                               updateHandler=None,
                               isKey=False,
                               readOnly=True,
                               description=""):
        prop = {'name': name, 'label': label, 'type': 'multiselect'}
        if isKey is True:
            prop['isKey'] = True
            if self.entrykey is not None:
                raise KeyError("DataView '{}' already have a key ({}) and cant be overridden with {}".format(
                    self.name, self.entrykey, name))
            self.entrykey = name
        prop['readOnly'] = readOnly
        prop['selection'] = selectables
        prop['group'] = group
        prop['description'] = description
        self.dataUpdateHandler[str(name)] = updateHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addActionProperty(self,
                          name,
                          label,
                          action,
                          icon,
                          actionHandler=None,
                          isKey=False,
                          readOnly=True,
                          color='red',
                          description=""):
        prop = {'name': name, 'label': label, 'type': 'action'}
        prop['isKey'] = False
        prop['icon'] = icon
        prop['color'] = color
        prop['action'] = action
        prop['description'] = description
        self.dataAction[str(action)] = actionHandler
        self.properties.append(prop)
        self.entryPropList[name] = None

    def addRemoveEntryOption(self, name, label):
        prop = {'name': name, 'label': label, 'type': 'remove'}
        prop['isKey'] = False
        prop['icon'] = 'delete'
        self.properties.append(prop)

    def emitUpdate(self, key, property, value):
        self.dataUpdates.append({'key': key, 'property': property, 'value': value, 'view': self.uri})

    def emitSyncUpdate(self, key, view=None, workspace=None):
        if view is None:
            view = self.uri

        self.dataSyncs.append({'type': 'update', 'key': key, 'view': view, 'workspace': workspace})

    def emitSyncRemove(self, key, view=None, workspace=None):
        if view is None:
            view = self.uri

        self.dataSyncs.append({'type': 'remove', 'key': key, 'view': view, 'workspace': workspace})

    def emitSyncCreate(self, key, view=None, workspace=None):
        if view is None:
            view = self.name

        self.dataSyncs.append({'type': 'create', 'key': key, 'view': view, 'workspace': workspace})

    # Handler for getting the freshly build view
    def getViewHandler(self, user, workspace, query=None):
        raise NotImplementedError

    # Handler for getting the views meta-data
    def getViewMetaHandler(self, user, workspace):
        return {}

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace):
        raise NotImplementedError

    # Handler for a request to remove a view entry
    def removeViewEntryHandler(self, user, workspace, key):
        raise NotImplementedError

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        raise NotImplementedError

    # Handler for view actions
    def executeViewActionHandler(self, user, workspace, action):
        try:
            return self.dataAction[action.viewAction](user, workspace, action, action.entry[self.entrykey])
        except Exception:
            return self.dataAction[action.viewAction](user, workspace, action.entry[self.entrykey])

    def defineProperties(self):
        pass

    def defineMetadata(self):
        pass
