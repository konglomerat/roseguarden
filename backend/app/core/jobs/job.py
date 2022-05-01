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

from datetime import datetime
from core.logs import logManager


class Job(object):
    """Base class that each job inherit from.
       The class define methods that all jobs have to implement
    """
    description = "Not available"  # description of the job
    disable = False  # disable the job
    local = True  # only runable by the same workspace
    strict = True  # strict argument parsing
    requireAdmin = False  # admin is required to view the page
    requirePermission = None  # a permission is required in the meaning of one of the following

    # Repetetive members
    cron = False  # see https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html for the encoding
    day = None
    week = None
    day_of_week = None
    hour = None
    minute = None
    second = None

    def __init__(self, name=None, uri=None):
        if name is None:
            self.name = type(self).__name__
        else:
            self.name = name
        self.job_key = self.name
        self.workspace = ""
        self.parameters = None
        self.defineArguments()

    def start_job(self, **kwargs):
        from core import create_app, db
        from core.jobs.models import JobExecute

        self.app, _ = create_app(True)
        self.db = db
        self.app.app_context().push()
        triggered = datetime.now()
        current_time = triggered.strftime("%H:%M:%S")
        logManager.info("Run " + self.name + " " + current_time)

        je = None
        if 'job_execution_id' in kwargs:
            je = JobExecute.query.filter_by(id=kwargs['job_execution_id']).first()

        if je is None:
            je = JobExecute()
            je.workspace = self.workspace
            je.triggered_by = "Cron"
            je.triggered_on = triggered
            je.name = self.job_key
            self.db.session.add(je)
            self.db.session.commit()

        try:
            self.run(**kwargs)
            je.state = "SUCCEED"
            je.results = {"hjsadhj": "jklsajdklas"}
        except Exception as e:
            je.state = "FAILED"
            print(e)

        after = datetime.now()
        delta = after - triggered
        je.lifetime = delta.total_seconds()
        self.db.session.commit()

    def addArgument(self, name, typestring, label="", description="", optional=False, group=None):
        p = {'name': name, 'type': typestring, 'label': label, 'optional': optional, 'group': group}
        if self.parameters is None:
            self.parameters = [p]
        else:
            self.parameters.append(p)

    def addDictArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add dict type argument to job {}".format(self.name))
        self.addArgument(name, 'dict', label, description, optional, group)

    def addListArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add list type argument to job {}".format(self.name))
        self.addArgument(name, 'list', label, description, optional, group)

    def addStringArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add string type argument to job {}".format(self.name))
        self.addArgument(name, 'string', label, description, optional, group)

    def addDoubleArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add double type argument to job {}".format(self.name))
        self.addArgument(name, 'double', label, description, optional, group)

    def addIntegerArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add integer type argument for job {}".format(self.name))
        self.addArgument(name, 'integer', label, description, optional, group)

    def addDatetimeArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add datetime type argument for job {}".format(self.name))
        self.addArgument(name, 'datetime', label, description, optional, group)

    def addTimeArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add time type argument for job {}".format(self.name))
        self.addArgument(name, 'time', label, description, optional, group)

    def addDateArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add date tyme argument for job {}".format(self.name))
        self.addArgument(name, 'date', label, description, optional, group)

    def addBooleanArgument(self, name, label="", description="", optional=False, group=None):
        logManager.info("Add boolean type argument for job {}".format(self.name))
        self.addArgument(name, 'boolean', label, description, optional, group)

    def defineArguments(self):
        pass

    def run(self, *args, **kwargs):
        raise NotImplementedError
