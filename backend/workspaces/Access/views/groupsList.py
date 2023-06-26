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

import arrow

from core.workspaces.workspace import Workspace
from core.workspaces.dataView import DataView
from core.users.models import User

from workspaces.Access.models import SpaceAccessGroup, SpaceAccessSpace
from workspaces.Access.types import (
    SpaceAccessType,
    SpaceAccessRechargePeriod,
    SpaceAccessEntryAccounting,
)

from workspaces.Access.access import (
    needs_the_accesstype_a_budget,
    do_accesstype_use_group_budget,
    do_accesstype_gets_recharge,
)

""" A view contaning the list of accessGroups
"""


class AccessGroupsList(DataView):
    uri = "accessGroupsList"
    requireLogin = True

    def defineProperties(self):
        self.addIntegerProperty(name="id", label="ID", isKey=True)
        self.addStringProperty(name="name", label="Name")
        self.addStringProperty(name="note", label="Note")
        self.addSelectProperty(
            name="type",
            label="Access type",
            selectables=[e.value for e in SpaceAccessType],
        )
        self.addTimeProperty(name="daily_start_time", label="Daily start time")
        self.addTimeProperty(name="daily_end_time", label="Daily end time")
        self.addMultiSelectProperty(name="spaces", label="Space keys", selectables=[])
        self.addIntegerProperty(name="days_mask", label="Accessable days")
        self.addBooleanProperty(name="expires_as_default", label="Expires (as default)")
        self.addIntegerProperty(name="expires_after_days_default", label="Expires (days default)")
        self.addBooleanProperty(name="budget_needed", label="Need budget")
        self.addBooleanProperty(name="use_group_budget", label="Accounts group budget")
        self.addIntegerProperty(name="group_budget", label="Group budget")
        self.addIntegerProperty(name="start_budget", label="Start budget")
        self.addBooleanProperty(name="budget_gets_recharge", label="Do recharged")
        self.addIntegerProperty(name="recharge_budget_amount", label="Recharge amount")
        self.addSelectProperty(
            name="recharge_budget_period",
            label="Used periods for recharge",
            selectables=[e.value for e in SpaceAccessRechargePeriod],
        )
        self.addSelectProperty(
            name="entry_accounting",
            label="Account entry by",
            selectables=[e.value for e in SpaceAccessEntryAccounting],
        )
        self.addIntegerProperty(name="recharge_budget_every_periods", label="Recharge every")
        self.addBooleanProperty(name="recharge_budget_gets_cutoff", label="Recharge gets cut")
        self.addIntegerProperty(name="recharge_budget_cutoff_max", label="Expires (days default)")

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for AccessGroupsList")
        entrylist = []
        all_groups = SpaceAccessGroup.query.all()
        for g in all_groups:
            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = g.id
            entry.name = g.name
            entry.note = g.note
            entry.type = g.access_type.value
            entry.entry_accounting = g.entry_accounting_type.value
            entry.daily_start_time = g.daily_access_start_time.format("HH:mm")
            entry.daily_end_time = g.daily_access_end_time.format("HH:mm")
            entry.spaces = []
            for si in g.spaces:
                entry.spaces.append(si.id)

            entry.days_mask = g.day_access_mask
            entry.expires_as_default = g.access_expires_as_default
            entry.expires_after_days_default = g.access_expires_default_days
            entry.use_group_budget = do_accesstype_use_group_budget(g.access_type)
            entry.group_budget = g.group_budget
            entry.start_budget = g.access_default_start_budget
            entry.budget_needed = needs_the_accesstype_a_budget(g.access_type)
            entry.budget_gets_recharge = do_accesstype_gets_recharge(g.access_type)
            entry.recharge_budget_amount = g.access_recharge_budget_amount
            entry.recharge_budget_period = g.access_recharge_budget_period.value
            entry.recharge_budget_every_periods = g.access_recharge_budget_every_periods
            entry.recharge_budget_gets_cutoff = g.access_recharge_budget_get_cutoff
            entry.recharge_budget_cutoff_max = g.access_recharge_budget_cutoff_max

            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return "<{} with {} properties>".format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        ag = SpaceAccessGroup()
        if hasattr(entry, "name"):
            ag.name = entry.name
        else:
            ag.name = "New group"
        ag.note = "Add a note here"
        ag.group_budget = 10
        workspace.db.session.add(ag)
        self.emitSyncCreate(ag.id, "accessGroupsList")
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
        ag = SpaceAccessGroup.query.filter_by(id=key).first()
        sas = SpaceAccessSpace.query.all()

        if ag is None:
            raise Exception("Update failed, group not found")
        if hasattr(entry, "spaces"):
            ag.spaces.clear()
            for n in sas:
                if n.id in entry["spaces"]:
                    print(n, n.id)
                    ag.spaces.append(n)
        if hasattr(entry, "name"):
            ag.name = entry.name
        if hasattr(entry, "note"):
            ag.note = entry.note
        if hasattr(entry, "daily_start_time"):
            ag.daily_access_start_time = arrow.get(entry.daily_start_time, "HH:mm")
        if hasattr(entry, "daily_end_time"):
            ag.daily_access_end_time = arrow.get(entry.daily_end_time, "HH:mm")
        if hasattr(entry, "days_mask"):
            ag.day_access_mask = entry.days_mask
        if hasattr(entry, "expires_as_default"):
            ag.access_expires_as_default = entry.expires_as_default
        if hasattr(entry, "expires_after_days_default"):
            ag.access_expires_default_days = entry.expires_after_days_default
        if hasattr(entry, "type"):
            ag.access_type = SpaceAccessType(entry.type)
            ag.access_use_group_budget = do_accesstype_use_group_budget(ag.access_type)
            ag.access_need_budget = needs_the_accesstype_a_budget(ag.access_type)
            ag.access_gets_recharged = do_accesstype_gets_recharge(ag.access_type)
        if hasattr(entry, "group_budget"):
            ag.group_budget = entry.group_budget
        if hasattr(entry, "start_budget"):
            ag.access_default_start_budget = entry.start_budget
        if hasattr(entry, "recharge_budget_amount"):
            ag.access_recharge_budget_amount = entry.recharge_budget_amount
        if hasattr(entry, "recharge_budget_period"):
            ag.access_recharge_budget_period = SpaceAccessRechargePeriod(entry.recharge_budget_period)
        if hasattr(entry, "recharge_budget_every_periods"):
            ag.access_recharge_budget_every_periods = entry.recharge_budget_every_periods
        if hasattr(entry, "recharge_budget_gets_cutoff"):
            ag.access_recharge_budget_get_cutoff = entry.recharge_budget_gets_cutoff
        if hasattr(entry, "recharge_budget_cutoff_max"):
            ag.access_recharge_budget_cutoff_max = entry.recharge_budget_cutoff_max
        self.emitSyncUpdate(key)

    # Handler for a request to update a single view entry
    def removeViewEntryHandler(self, user, workspace, key):
        print("Handle removeViewEntryHandler request for " + self.uri)
        ag = SpaceAccessGroup.query.filter_by(id=key).first()
        workspace.db.session.delete(ag)
        self.emitSyncRemove(key)
