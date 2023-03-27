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

from core.jobs.job import Job
from core.users.models import User
from core.logs import logManager
from workspaces.Access.types import SpaceAccessType, SpaceAccessRechargePeriod
from workspaces.Access.models import SpaceAccessGroup
import arrow


class UpdateBudgetsJob(Job):
    cron = True
    second = "0"
    minute = "0"
    hour = "1"
    day = "*"
    disable = False
    description = "Updates user access budgets for all groups"

    def needs_update(self, group):
        # get the actual date and time
        now = arrow.utcnow()

        # check for access_last_group_recharge_at is valid
        # if not reset to utc-now
        if group.access_last_group_recharge_at is None:
            group.access_last_group_recharge_at = now
            return False

        # check for recharge
        if group.access_gets_recharged is False:
            return False

        # compute the next recharge date
        # default is None
        next_recharge_date = None

        # compute for monthly recharge
        if group.access_recharge_budget_period == SpaceAccessRechargePeriod.MONTHS:
            next_recharge_date = group.access_last_group_recharge_at.shift(
                months=group.access_recharge_budget_every_periods
            )
            # recharge executes on first of month 00:01
            next_recharge_date = next_recharge_date.replace(day=1, hour=0, minute=0, second=1)

        # compute for weekly recharge
        if group.access_recharge_budget_period == SpaceAccessRechargePeriod.WEEKS:
            next_recharge_date = group.access_last_group_recharge_at.shift(
                days=-group.access_last_group_recharge_at.weekday(),  # recharge executed on Mondays
                weeks=group.access_recharge_budget_every_periods,
            )
            next_recharge_date = next_recharge_date.replace(hour=0, minute=0, second=1)

        print(next_recharge_date)
        # check for recharge is needed and due date
        if next_recharge_date is not None and now > next_recharge_date:
            logManager.info(f"Access budget update needed for {group.name}")
            return True
        return False

    def run(self, **kwargs):
        logManager.info("Updates budget for users in all access groups")
        all_groups = SpaceAccessGroup.query.all()
        # iterate through all groups
        for g in all_groups:
            # check if budget update is needed
            if self.needs_update(g):
                # recharge the group budget
                if g.access_type == SpaceAccessType.AUTO_RECHARGED_GROUP_BUDGET:
                    g.group_budget += g.access_recharge_budget_amount  # add budget
                    # check for cutoff is enabled / needed
                    if g.access_recharge_budget_get_cutoff:
                        if g.group_budget > g.access_recharge_budget_cutoff_max:
                            g.group_budget = g.access_recharge_budget_cutoff_max

                # recharge all user budgets in group
                if g.access_type == SpaceAccessType.AUTO_RECHARGED_USER_BUDGET:
                    for u in g.users:
                        u.access.access_budget += g.access_recharge_budget_amount  # add budget
                        u.access_last_user_recharge_at = arrow.utcnow()  # update users recharge date
                        # check for cutoff is enabled / needed
                        if g.access_recharge_budget_get_cutoff:
                            if u.access.access_budget > g.access_recharge_budget_cutoff_max:
                                u.access.access_budget = g.access_recharge_budget_cutoff_max

                # update groups recharge date
                g.access_last_group_recharge_at = arrow.utcnow()
            print(g)
