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

from core import db

association_table_user_permissiongroup = db.Table(
    'permissiongroup_user_map', db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('permissiongroup_id', db.Integer, db.ForeignKey('permissiongroups.id')))


class PermissionGroup(db.Model):
    __tablename__ = 'permissiongroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default="")
    ldap_group = db.Column(db.String(64), default="")
    description = db.Column(db.String(128), default="")
    ldap = db.Column(db.Boolean, default=False)
    users = db.relationship(
        "User",
        backref="permission_groups",
        secondary=association_table_user_permissiongroup,
        lazy='subquery',
    )


association_table_permission_permissiongroup = db.Table(
    'permission_permissiongroup_map', db.Column('permissiongroup_id', db.Integer,
                                                db.ForeignKey('permissiongroups.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    groups = db.relationship(
        "PermissionGroup",
        backref="permissions",
        secondary=association_table_permission_permissiongroup,
        lazy='subquery',
    )
    name = db.Column(db.String(64), default="")
    description = db.Column(db.String(128), default="")

    def __repr__(self):
        return '<Permission "{}">'.format(self.name)
