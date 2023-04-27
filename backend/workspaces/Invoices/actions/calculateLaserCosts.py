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

    def calculate_costs(self, time_in_minutes, is_member):
        # extract coefficents
        (a, b, c) = self.get_price_coefficients(is_member)
        # costs of first minute
        costs_first_minute = a * math.exp(-b) + c
        # costs of last minute
        costs_last_minute = a * math.exp(-b * time_in_minutes) + c
        # the total price is the integral of the price_per_minute function
        costs_tax_excluded = a / b * (1 - math.exp(-b * time_in_minutes)) + c * time_in_minutes
        tax = round(costs_tax_excluded * 0.19, 2)
        return round(costs_tax_excluded, 2), tax, round(costs_first_minute, 2), round(costs_last_minute, 2)

    def handle(self, action, user, workspace, actionManager):
        try:
            (start_h, start_m, start_s) = [int(t) for t in action.get("counter_at_start").split(":")]
            (end_h, end_m, end_s) = [int(t) for t in action.get("counter_at_end").split(":")]
            seconds_at_start = (start_h * 60 + start_m) * 60 + start_s
            seconds_at_end = (end_h * 60 + end_m) * 60 + end_s
            usage_in_minutes = (seconds_at_end - seconds_at_start) / 60
            minutes= int(usage_in_minutes)
            seconds = round(usage_in_minutes % 1 * 60) 
            membership = action["membership"] == "member"
        except Exception as e:
            return "success", [], {"costs_in_euro": None}

        costs, tax, cost_first_minute, cost_last_minute = self.calculate_costs(
            time_in_minutes=usage_in_minutes, is_member=membership
        )
        return (
            "success",
            [],
            {
                "usage": f"{minutes} min {seconds} s".replace(".", ","),
                "costs": f"{costs} €".replace(".", ","),
                "tax": f"{tax} €".replace(".", ","),
                "total_costs": f"{round(costs+tax,2)} €".replace(".", ","),
                "costs_first_minute": f"{cost_first_minute} €/min".replace(".", ","),
                "costs_last_minute": f"{cost_last_minute} €/min".replace(".", ","),
                "average_costs_per_minute": f"{round(costs / usage_in_minutes,2)} €/min".replace(".", ","),
            },
        )
