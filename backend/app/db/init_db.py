"""
This module takes care of the initialization of the database if Alembic is not set up
"""

from app.db.base import Base
from app.db.session import engine

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db() -> None:
    """
    Creates all tables in the database
    This function will not be used in production cause Alembic will take care of the initialization of the database
    """
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # pylint: disable=no-member
    Base.metadata.create_all(bind=engine)
