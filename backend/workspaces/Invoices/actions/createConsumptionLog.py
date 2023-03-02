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
from core.logs import logManager
from core.actions import webclientActions
from core.users import userManager
from core.messages import send_mail, send_message
from core.actions import generateActionLink

from workspaces.Invoices.models import ConsumptionLog


class CreateConsumptionLog(Action):
    def __init__(self, app):
        # logManager.info("Register of type Action created")
        super().__init__(app, uri="createConsumptionLog")

    def handle(self, action, user, workspace, actionManager):
        replyActions = []

        consumption_log = ConsumptionLog()
        consumption_log.consumed_as_guest = True
        consumption_log.guest_email = "konglomerat@konglomerat.org"
        consumption_log.guest_is_member = True
        consumption_log.service_area = "Laser"
        consumption_log.service_name = "Cameo"
        consumption_log.service_quantity = 42.0
        consumption_log.service_unit = "min"

        workspace.db.session.add(consumption_log)

        replyActions.append(webclientActions.NotificationAction.generate("Consumption log created", "success"))
        return "success", replyActions
