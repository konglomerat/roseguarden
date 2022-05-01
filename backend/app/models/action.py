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

# from core import db
from sqlalchemy_utils import ArrowType
import arrow

from sqlalchemy import VARCHAR, CheckConstraint, Column, String, Integer, Boolean

from app.db.base_class import Base

from core.common.jsonDict import JsonDict


class ActionLink(Base):
    # __tablename__ = 'actionlinks'
    # nonvolatile data stored in the db
    # id = Column(Integer, primary_key=True)  # < will created with Base class
    hash = Column(String(128), default="")
    workspace = Column(String(120), default="")
    need_login = Column(Boolean, default=True)
    action = Column(String(120), default="")
    action_data_json = Column(JsonDict)
    run_only_once = Column(Boolean, default=True)
    expire_on_date = Column(ArrowType, default=arrow.utcnow)
    redirect_to = Column(String(255), default="")

    def __repr__(self):
        return "<ActionLink {} for {}/{} [expires on {}] >".format(
            self.link, self.workspace, self.action, self.expire_on_date
        )
