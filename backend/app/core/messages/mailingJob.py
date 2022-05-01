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

import smtplib
import imaplib
import time
from email.mime.text import MIMEText
from jinja2 import Template
from core.jobs.job import Job


class MailFromFileTemplateJob(Job):

    description = "Send a mail from a local template file with data"

    def defineArguments(self):
        self.addListArgument('recipients', label="Recipients", description="List of recipients email adresses")
        self.addStringArgument('subject', label="Subject", description="Subject of the mail")
        self.addStringArgument('template_path', label="Template path", description="File path to the template")
        self.addDictArgument('data', label="Template data", description="Data for the template")

    def run(self, **kwargs):
        config = kwargs['mail_config']
        subject = kwargs['subject']
        recipients = kwargs['recipients']
        template_path = kwargs['template_path']
        data = kwargs['data']

        sender = config.get('sender')

        # Get File Content in String
        jinja2_template_string = open(template_path, 'r').read()

        # Create Template Object
        template = Template(jinja2_template_string)

        content = template.render(**data)
        # print(content)

        # Render HTML Template String
        try:
            msg = MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ','.join(recipients)

            host = config.get('server')
            port = config.get('port')
            username = config.get('username')
            password = config.get('password')
            s = smtplib.SMTP_SSL(host, port)
            s.login(username, password)
            s.send_message(msg)
            s.quit()

            save_sent_mails = config.get('save_sent_mails')
            if save_sent_mails:
                text = msg.as_string()
                imap_port = config.get('imap_port')
                imap_sent_folder = config.get('imap_sent_folder')
                try:
                    imap = imaplib.IMAP4_SSL(host, imap_port)
                    imap.login(username, password)
                    imap.append(imap_sent_folder, '\\Seen', imaplib.Time2Internaldate(time.time()),
                                text.encode('utf8'))
                    imap.logout()
                except Exception as e:
                    print("Unable to copy email to send folder:", e)
                    raise e
        except Exception as e:
            print(e)
            raise e
