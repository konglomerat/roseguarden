from logging.config import fileConfig
import logging
from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sqlalchemy_utils  # noqa: F401

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

al_logger = logging.getLogger("alembic.runtime.migration")
al_logger.setLevel(logging.ERROR)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
import os
import sys
from pathlib import Path


file = Path(__file__).resolve()
parent, top, root = file.parent, file.parents[4], file.parents[5]

sys.path.append(str(top))
sys.path.append(str(file.parents[2]))

logger.info(f"cwd {os.getcwd()} {top} {root} {file.parents[2]}")

# fixme: set this per workspace
alembic_datatable_name = "migration_version_" + (str(file.parents[2].name)).lower()
print(alembic_datatable_name)
from core import db
import models
from config import configure_app, load_config

target_metadata = db.Model.metadata

# fixme: this is probably fine for our use case, but in configure_app()
# we also allow setting from os.environ.get('DATABASE_URL')
app_config = load_config("config.ini")
database_path = app_config["SYSTEM"].get("database_path", None)
basedir = file.parents[4]

config.set_main_option(
    "sqlalchemy.url", database_path or os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def include_object(obj, name, type_, reflected, compare_to):
    """
    Should you include this table or not?
    """
    if reflected is False:
        if type(obj) == type(compare_to):
            logger.info(f"No changes on {name}")
        else:
            logger.info(f"Changes found for {name}")
        return True
    return False


def render_item(type_, obj, autogen_context):
    # custom render for sqalchemy_utils ChoiceType column and params
    # May be better to use: https://stackoverflow.com/questions/30132370/trouble-when-using-alembic-with-sqlalchemy-utils
    print(type(obj))
    if type_ == "type" and type(obj).__name__ == "IntEnum":
        col_type = "sa.Integer(), default=0"
        return col_type
    if type_ == "type" and type(obj).__name__ == "IntFlag":
        col_type = "sa.Integer(), default=0"
        return col_type

    # default rendering for other objects
    return False


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            include_object=include_object,
            version_table=alembic_datatable_name,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
