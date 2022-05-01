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


class UpdateBudgetsWeeklyJob(Job):
    cron = True
    second = "0"
    minute = "0"
    hour = "1"
    day_of_week = "mon"
    disable = False
    description = "Update the account for weekly access budget users"

    def run(self, **kwargs):
        logManager.info("Updated budget of all user (weekly)")
        all_user = User.query.filter_by(account_locked=False).all()
        for u in all_user:
            u.budget = 10
