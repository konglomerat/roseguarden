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

from core.common.deface import deface_string_end, deface_string_middle

from core.users.models import User

from workspaces.Invoices.models import ConsumptionLog

""" A view contaning a list of all consumed logs
"""


class ConsumedList(DataView):
    uri = "consumedList"
    requireLogin = True

    def defineProperties(self):
        self.addIntegerProperty(name="id", label="Id", isKey=True, hide=True)
        self.addDatetimeProperty(name="consumed_at", label="Date")
        self.addStringProperty(name="consumed_by", label="User")
        self.addStringProperty(name="service", label="Service")
        self.addStringProperty(name="amount", label="Amount")
        self.addStringProperty(name="details", label="Details")

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for AuthenticatorRequestList")

        entrylist = []
        all_consume_logs = ConsumptionLog.query.all()
        cl: ConsumptionLog
        for cl in all_consume_logs:
            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = cl.id
            entry.consumed_at = cl.consumed_at.format("YYYY-MM-DD HH:mm")
            entry.service = f"[{cl.service_area}] {cl.service_name}"
            entry.amount = f"{cl.service_quantity} {cl.service_unit}"
            if cl.linked_user is None or cl.consumed_as_guest:
                entry.consumed_by = "(Guest) " + str(cl.guest_email)
            else:
                entry.consumed_by = f"{cl.linked_user.firstname} {cl.linked_user.lastname} ({cl.linked_user.email})"
            entry.details = f"{cl.project_purpose}"

            entrylist.append(entry.extract())
        return entrylist

    def __repr__(self):
        return "<{} with {} properties>".format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
