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

from core.logs import logManager
import arrow
from jinja2 import Template
from core.jobs import jobManager, add_dated_job
from core.messages.mailingJob import MailFromFileTemplateJob


class MessageManager(object):
    """ The MessageManager ...
    """
    def __init__(self, ):
        # preparation to instanciate
        self.config = None
        self.app = None
        self.db = None
        self.workspaceManager = None

    def add_message(self,
                    recipient_user,
                    subject,
                    message_template_path,
                    data,
                    sender,
                    mail=True,
                    mail_template_path=None):
        if mail is True and mail_template_path is not None:
            user_mail = recipient_user.email
            self.add_mail_job([user_mail], subject, mail_template_path, data)
        # Add the Message
        # Get File Content in String
        jinja2_template_string = open(message_template_path, 'r').read()

        # Create Template Object
        template = Template(jinja2_template_string)

        content = template.render(**data)

        m = self.message()
        m.message_html = content
        m.subject = subject
        m.recipient = recipient_user
        m.sender_name = sender
        m.message_send_date = arrow.utcnow()
        self.db.session.add(m)

    def add_mail_job(self, recipients, subject, template_path, data):
        args = {
            'mail_config': self.config['MAIL'],
            'recipients': recipients,
            'subject': subject,
            'template_path': template_path,
            'data': data
        }
        add_dated_job(None, MailFromFileTemplateJob(), args)

    def init_manager(self, app, db, workspaceManager, config):
        self.config = config
        self.app = app
        self.db = db
        self.workspaceManager = workspaceManager

        from core.messages.models import Message
        self.message = Message

        jobManager.register_job(None, MailFromFileTemplateJob)

        logManager.info("MessageManager initialized")
