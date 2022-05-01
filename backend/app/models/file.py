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
import enum
from sqlalchemy import Table, Column, String, Integer, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.db.base_class import Base

association_table_user_filepermissiongroup = Table(
    "filepermissiongroup_user_map",
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("filepermissiongroup_id", Integer, ForeignKey("filepermissiongroups.id")),
)


class FilePermissionGroup(Base):
    name = Column(String(64), default="")
    ldap_group = Column(String(64), default="")
    ldap = Column(Boolean, default=False)
    users = relationship(
        "User",
        backref="filepermission_groups",
        secondary=association_table_user_filepermissiongroup,
        lazy="subquery",
    )

    def __init__(self, name):
        self.name = name


association_table_filepermission_filepermissiongroup = Table(
    "filepermission_filepermissiongroup_map",
    Column("filepermissiongroup_id", Integer, ForeignKey("filepermissiongroups.id")),
    Column("filepermission_id", Integer, ForeignKey("filepermissions.id")),
)


class FilePermissionAccess(enum.IntFlag):
    NONE = 0
    READ = 1
    WRITE = 2


class FilePermission(Base):
    access = Column(Enum(FilePermissionAccess), default=FilePermissionAccess.NONE)
    groups = relationship(
        "FilePermissionGroup",
        backref="filepermissions",
        secondary=association_table_filepermission_filepermissiongroup,
        lazy="subquery",
    )
    ldap_group = Column(String(64), default="")
    ldap = Column(Boolean, default=False)
    name = Column(String(64), default="")
    description = Column(String(128), default="")

    def __repr__(self):
        return '<FilePermission "{}">'.format(self.name)


association_table_filepermission_filestorage = Table(
    "filepermission_filestorage_map",
    Column("filestorage_id", Integer, ForeignKey("filestorage.id")),
    Column("filepermission_id", Integer, ForeignKey("filepermissions.id")),
)


class FileStorageType(enum.IntFlag):
    LOCAL = 1
    NETWORK = 2
    USER = 4
    WORKSPACE = 8


class FileStorage(Base):
    # nonvolatile data stored in the db
    path = Column(String(120), default="")
    storage_type = Column(Enum(FileStorageType))
    permissions = relationship(
        "FilePermission",
        backref="filestorages",
        secondary=association_table_filepermission_filestorage,
        lazy="subquery",
    )

    def __repr__(self):
        return "<FileStorage {} of type:{}>".format(self.path, self.storage_type)


class GeneratedFile(Base):
    # nonvolatile data stored in the db
    path = Column(String(120), default="")
    generated_on_date = Column(ArrowType, default=arrow.utcnow)
    expire_on_date = Column(ArrowType, default=arrow.utcnow)
    size_in_bytes = Column(Integer, default=0)
    filestorage_id = Column(Integer, ForeignKey("filestorage.id"))
    filestorage = relationship(
        "FileStorage", backref=backref("generatedfiles", uselist=True)
    )

    def __repr__(self):
        return "<GeneratedFile {} of type:{}>".format(self.path, self.generated_on_date)


class UploadedFile(Base):
    # nonvolatile data stored in the db
    path = Column(String(120), default="")
    generated_on_date = Column(ArrowType, default=arrow.utcnow)
    expire_on_date = Column(ArrowType, default=arrow.utcnow)
    size_in_bytes = Column(Integer, default=0)
    filestorage_id = Column(Integer, ForeignKey("filestorage.id"))
    filestorage = relationship(
        "FileStorage", backref=backref("uploadedfiles", uselist=True)
    )

    def __repr__(self):
        return "<UploadedFile {} of type:{}>".format(self.path, self.generated_on_date)
