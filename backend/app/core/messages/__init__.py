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

import os
from flask import Blueprint
from core.messages.messageManager import MessageManager

messages_bp = Blueprint('messages', __name__)

messageManager = MessageManager()


def send_mail(recipients, subject, workspace, mail_template, data):
    template_path = mail_template
    if workspace is not None:
        template_path = os.path.join(workspace.path, 'templates', mail_template)
    messageManager.add_mail_job(recipients, subject, template_path, data)


def send_message(recipient_user,
                 subject,
                 workspace,
                 message_template,
                 data,
                 sender="System",
                 mail=False,
                 mail_template=None):
    if workspace is not None:
        template_path = os.path.join(workspace.path, 'templates', message_template)

    mail_template_path = mail_template
    if mail is True:
        if workspace is not None and mail_template_path is not None:
            template_path = os.path.join(workspace.path, 'templates', mail_template)

    messageManager.add_message(recipient_user, subject, template_path, data, sender, mail, mail_template_path)


from core.messages import routes  # noqa: F401
