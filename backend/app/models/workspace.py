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

from app.db.base_class import Base
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

association_table_user_permissiongroup = Table(
    "permissiongroup_user_map",
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("permissiongroup_id", Integer, ForeignKey("permissiongroups.id")),
)


class PermissionGroup(Base):
    __tablename__ = "permissiongroups"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), default="")
    ldap_group = Column(String(64), default="")
    description = Column(String(128), default="")
    ldap = Column(Boolean, default=False)
    users = relationship(
        "User",
        backref="permission_groups",
        secondary=association_table_user_permissiongroup,
        lazy="subquery",
    )


association_table_permission_permissiongroup = Table(
    "permission_permissiongroup_map",
    Column("permissiongroup_id", Integer, ForeignKey("permissiongroups.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    groups = relationship(
        "PermissionGroup",
        backref="permissions",
        secondary=association_table_permission_permissiongroup,
        lazy="subquery",
    )
    name = Column(String(64), default="")
    description = Column(String(128), default="")

    def __repr__(self):
        return '<Permission "{}">'.format(self.name)
