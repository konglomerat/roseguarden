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

from core.common.jsonDict import JsonDict


class Node(db.Model):
    __tablename__ = 'nodes'
    # nonvolatile data stored in the db
    id = db.Column(db.Integer, primary_key=True)
    _authentification_hash = db.Column(db.Binary(128))
    name = db.Column(db.String(64), index=True, unique=True)
    fingerprint = db.Column(db.String(120), default="")
    class_name = db.Column(db.String(120), default="")
    class_id = db.Column(db.String(120), default="")
    class_workspace = db.Column(db.String(120), default="")
    identification_hash = db.Column(db.String(120), default="")
    identification = db.Column(JsonDict)
    last_request_on = db.Column(ArrowType, default=arrow.utcnow)
    authorization_status = db.Column(db.String(120), default="Not authorized")
    authorized = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(120), default="Not active")

    def __repr__(self):
        return '<Node {} [{}] >'.format(self.name, self.fingerprint)

    def __init__(self, name, fingerprint, authentification):
        self.name = name
        self.fingerprint = fingerprint
        self.authentification = authentification

    @hybrid_property
    def authentification(self):
        return self._authentification_hash

    @authentification.setter
    def authentification(self, plaintext_authentification):
        self._authentification_hash = bcrypt.generate_password_hash(plaintext_authentification)

    @hybrid_method
    def checkAuthentification(self, plaintext_authentification):
        return bcrypt.check_password_hash(self.authentification, plaintext_authentification)


class NodeSettings(db.Model):
    __tablename__ = 'node_settings'
    # nonvolatile data stored in the db
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    node = db.relationship("Node", backref=db.backref("settings", uselist=True))


class NodeLog(db.Model):
    __tablename__ = 'node_logs'
    id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(120), default="UNKNOWN")
    node_fingerprint = db.Column(db.String(120), default="")
    node_authetification_status = db.Column(db.String(120), default="")
    node_ip = db.Column(db.String(120), default="")
    node_status = db.Column(db.String(120), default="")
    node_uptime = db.Column(db.Integer, default=0)
    node_logcounter = db.Column(db.Integer, default=0)
    node_errorcounter = db.Column(db.Integer, default=0)
    node_timestamp = db.Column(ArrowType, default=arrow.utcnow)
    request_source = db.Column(db.String(120), default="")
    request_actions = db.Column(db.String(250), default="")
    request_reply = db.Column(db.String(120), default="")
    request_date = db.Column(ArrowType, default=arrow.utcnow)
