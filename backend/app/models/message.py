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

import arrow
from sqlalchemy_utils import ArrowType
from app.db.base_class import Base
from sqlalchemy import Column, String, ForeignKey, UnicodeText, Boolean
from sqlalchemy.orm import relationship, backref


class Message(Base):
    # nonvolatile data stored in the db
    recipient_email = Column(String, ForeignKey("users.email"))
    recipient = relationship("User", backref=backref("messages", uselist=True))
    sender_name = Column(String(120), default="")
    subject = Column(String(120), default="")
    message_html = Column(UnicodeText(), default="")
    message_send_date = Column(ArrowType, default=arrow.utcnow)
    message_read = Column(Boolean, default=False)

    def __repr__(self):
        return '<Message from {} to {} with subject "{}" [{}] >'.format(
            self.sender_name, self.recipient_name, self.subject, self.message_send_date
        )
