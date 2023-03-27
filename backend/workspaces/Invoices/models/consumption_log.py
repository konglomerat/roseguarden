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

from sqlalchemy_utils import ArrowType
import arrow

from core import db
from core.users.models import User


class ConsumptionLog(db.Model):
    __tablename__ = "invoice_consumption_log"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    consumed_as_guest = db.Column(db.Boolean, default=None)
    linked_user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="SET NULL"))
    linked_user = db.relationship("User", backref="consumptions", foreign_keys=linked_user_id)
    guest_is_member = db.Column(db.Boolean, default=None)
    guest_email = db.Column(db.String(128), default=None)

    consumed_at = db.Column(ArrowType, default=arrow.utcnow)
    created_at = db.Column(ArrowType, default=arrow.utcnow)

    service_area = db.Column(db.String(128), default=None)
    service_name = db.Column(db.String(128), default=None)
    service_quantity = db.Column(db.Float, default=None)
    service_unit = db.Column(db.String(128), default=None)

    project_name = db.Column(db.String(128), default=None)
    project_purpose = db.Column(db.String(128), default=None)
    project_details = db.Column(db.String(128), default=None)
