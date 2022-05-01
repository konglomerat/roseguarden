"""
This module contains the Base class for all database models
"""

import uuid
from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import registry

# To setup imperative mappings a mapper_registry must be created
# it will get imported from each python module which uses imperative mapping, in our case all bo4e related classes
mapper_registry = registry()

# pylint: disable=too-few-public-methods
@as_declarative()
class Base:
    """
    Base class for all database models
    All database models inheritate from this class to add basic columns like id, created_at and updated_at
    """

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow()
    )  # date of creation of entry
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )  # latest modification date
    __name__: str
    # Generate __tablename__ automatically
    # pylint: disable=no-self-argument
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Makes sure that table names are always lowercase
        """
        return cls.__name__.lower()
