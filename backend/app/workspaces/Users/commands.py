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

from flask import Blueprint
import click
import sqlite3
import os.path

from core import db
from core.users.models import User
from core.workspaces.commands import roseguarden_cli
from core.workspaces.workspaceHooks import WorkspaceHooks
from core.workspaces import workspaceManager

# Define your commands here

bp = Blueprint(__name__, __name__)


@roseguarden_cli.group()
@click.version_option()
def users():
    pass


@users.command('restore')
@click.argument('db_file')
def create(db_file):
    """ Restore user from an backup sqlite database
    """
    users = {}
    print(db_file)

    if not os.path.isfile(db_file):
        print("Database file dont exist")
        exit(1)

    with sqlite3.connect(db_file, ) as connection:
        c = connection.cursor()
        c.execute("SELECT * FROM users")

        rows = c.fetchall()

        columns = [column[0] for column in c.description]

        for row in rows:
            user_dict = dict(zip(columns, row))
            key = user_dict['email'].strip().lower()
            # print(key)
            users[user_dict['email'].strip().lower()] = user_dict

    user_blacklist = []
    all_user = User.query.all()
    for u in all_user:
        key = u.email.strip().lower()
        user_blacklist.append(key)

    # print(user_blacklist)
    for key, u in users.items():
        if key not in user_blacklist:
            new = User(key, "-")
            new._password_hash = u['_password_hash']
            new._authenticator_hash = u['_authenticator_hash']
            new.firstname = u['firstname'].strip()
            new.lastname = u['lastname'].strip()
            new.admin = u['admin']
            new.phone = u['phone'].strip()
            new.organization = u['organization'].strip()
            new.authenticator_status = u['authenticator_status']
            new.authenticator_changed_date = u['authenticator_changed_date']

            new.account_created_date = u['account_created_date']
            new.last_login_date = u['last_login_date']

            new.account_verified = u['account_verified']
            new.account_locked = u['account_locked']
            new.pinIsLocked = u['pinIsLocked']
            new.failedPinAttempts = u['failedPinAttempts']
            new.failedLoginAttempts = u['failedLoginAttempts']
            new.budget = u['budget']

            workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=new)

            print(new)
            db.session.add(new)

        else:
            print(f"skip {key}")
    db.session.commit()
