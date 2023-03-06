# General 

Place your models in this folder.

The core loads all models imported in `__init__.py`.

# Migrations

You might use the alembic command lines to setup migration here.

Run the command in the specific `models` folder

## Create a new revision in `versions`:

`alembic revision -m "name" --autogenerate --rev-id REV_ID`

Please use the actual naming convention. E.g. `-m "name" --autogenerate  --rev-id 000001`.

## Upgrade to a new revision:

`alembic upgrade REV_ID`

## Stamp to an actual version (may be needed before upgrade or create a new revision):

`alembic stamp --purge REV_ID`