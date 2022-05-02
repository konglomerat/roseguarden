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

from core import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy_utils import ArrowType
import arrow
from app.db.base_class import Base
from sqlalchemy import Column, String, Boolean, BINARY, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from core.common.jsonDict import JsonDict


class Node(Base):
    # nonvolatile data stored in the db
    _authentification_hash = Column(BINARY(128))
    name = Column(String(64), index=True, unique=True)
    fingerprint = Column(String(120), default="")
    class_name = Column(String(120), default="")
    class_id = Column(String(120), default="")
    class_workspace = Column(String(120), default="")
    identification_hash = Column(String(120), default="")
    identification = Column(JsonDict)
    last_request_on = Column(ArrowType, default=arrow.utcnow)
    authorization_status = Column(String(120), default="Not authorized")
    authorized = Column(Boolean, default=False)
    active = Column(Boolean, default=False)
    status = Column(String(120), default="Not active")

    def __repr__(self):
        return "<Node {} [{}] >".format(self.name, self.fingerprint)

    def __init__(self, name, fingerprint, authentification):
        self.name = name
        self.fingerprint = fingerprint
        self.authentification = authentification

    @hybrid_property
    def authentification(self):
        return self._authentification_hash

    @authentification.setter
    def authentification(self, plaintext_authentification):
        self._authentification_hash = bcrypt.generate_password_hash(
            plaintext_authentification
        )

    @hybrid_method
    def checkAuthentification(self, plaintext_authentification):
        return bcrypt.check_password_hash(
            self.authentification, plaintext_authentification
        )


class NodeSettings(Base):
    # nonvolatile data stored in the db
    node_id = Column(Integer, ForeignKey("nodes.id"))
    node = relationship("Node", backref=backref("settings", uselist=True))


class NodeLog(Base):
    __tablename__ = "node_logs"
    id = Column(Integer, primary_key=True)
    node_name = Column(String(120), default="UNKNOWN")
    node_fingerprint = Column(String(120), default="")
    node_authetification_status = Column(String(120), default="")
    node_ip = Column(String(120), default="")
    node_status = Column(String(120), default="")
    node_uptime = Column(Integer, default=0)
    node_logcounter = Column(Integer, default=0)
    node_errorcounter = Column(Integer, default=0)
    node_timestamp = Column(ArrowType, default=arrow.utcnow)
    request_source = Column(String(120), default="")
    request_actions = Column(String(250), default="")
    request_reply = Column(String(120), default="")
    request_date = Column(ArrowType, default=arrow.utcnow)
