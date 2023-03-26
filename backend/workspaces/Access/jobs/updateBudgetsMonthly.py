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


class UpdateBudgetsMonthlyJob(Job):
    cron = True
    second = "0"
    minute = "0"
    hour = "1"
    day = "*"
    disable = False
    description = "Update the account for monthly access budget users"

    def needs_update(self, group):
        now = arrow.utcnow()
        if group.access_last_group_recharge_at is None:
            group.access_last_group_recharge_at = now
        else:
            if group.access_recharge_budget_period == SpaceAccessRechargePeriod.MONTHS:
                next_recharge_date = group.access_last_group_recharge_at.shift(
                    days=-1, months=group.access_recharge_budget_every_periods
                )
                next_recharge_date = next_recharge_date.replace(day=1, hour=0, minute=0, second=1)
                print(next_recharge_date)

    def run(self, **kwargs):
        logManager.info("Updated budget of all user (monthly)")
        all_groups = SpaceAccessGroup.query.all()
        for g in all_groups:
            if g.access_gets_recharged:
                needs_update = self.needs_update(g)
                if g.access_type == SpaceAccessType.AUTO_RECHARGED_GROUP_BUDGET:
                    pass
                if g.access_type == SpaceAccessType.AUTO_RECHARGED_USER_BUDGET:
                    pass
            print(g)
