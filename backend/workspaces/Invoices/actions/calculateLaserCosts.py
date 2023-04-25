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

import math

from core.actions.action import Action
from core.logs import logManager
from core.actions import webclientActions
from core.users import userManager
from core.messages import send_mail, send_message
from core.actions import generateActionLink

from workspaces.Invoices.models import ConsumptionLog


class CalculateLaserCosts(Action):
    def __init__(self, app):
        # logManager.info("Register of type Action created")
        super().__init__(app, uri="calculateLaserCosts")

    def get_price_coefficients(self, is_member=False):
        if is_member:
            # Members
            price_at_t_0 = 0.8
            slope_at_t_0 = 0.01
            price_convergence = 0.3
        else:
            # Non-Members
            price_at_t_0 = 1.2
            slope_at_t_0 = 0.01
            price_convergence = 0.5

        a = price_at_t_0 - price_convergence
        b = slope_at_t_0 / a
        c = price_convergence
        return (a, b, c)

    def calculate_costs(self, time_in_minutes, is_member, include_tax):
        # extract coefficents
        (a, b, c) = self.get_price_coefficients(is_member)
        # time per minute
        costs_per_minute = a * math.exp(-b * time_in_minutes) + c
        # the total price is the integral of the price_per_minute function
        costs_tax_excluded = a / b * (1 - math.exp(-b * time_in_minutes)) + c * time_in_minutes
        # return cost with tax ex/included in €
        if include_tax:
            return round(costs_tax_excluded * 1.19, 2)
        else:
            return round(costs_tax_excluded, 2)

    def handle(self, action, user, workspace, actionManager):
        costs = self.calculate_costs(time_in_minutes=250.55, is_member=False, include_tax=True)
        return "success", [], {"costs_in_euro": costs}
