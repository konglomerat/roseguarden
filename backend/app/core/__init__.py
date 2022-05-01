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

import logging

from flask import Flask, Blueprint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy_utils import database_exists

from config import configure_app, load_config

from core.version import version
from core.logs import logManager
from core.workspaces import workspaceManager
from core.nodes import nodeManager
from core.users import userManager
from core.messages import messageManager
from core.jobs import jobManager
from core.actions import actionManager
from core.files import fileManager
from core.menus import menuBuilder

jwt = JWTManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app(minimal=False, config_file="config.ini", test=False):
    config = load_config(config_file)
    app = Flask(__name__, static_folder="./dist")
    # configure the app
    configure_app(app, config, test)

    if __name__ != '__main__' and test is False:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    # logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    if not minimal:
        CORS(app)
        logManager.init_app(app)
        logManager.info("Started roseguarden: " + version)
        jwt.init_app(app)
        workspaceManager.discoverModels()
        bcrypt.init_app(app)

    from core import app_bp  # noqa: F401
    app.register_blueprint(app_bp)

    from core.actions import actions_bp, models  # noqa: F401, F811
    app.register_blueprint(actions_bp)

    from core.users import auth_bp, models  # noqa: F401, F811
    app.register_blueprint(auth_bp)

    from core.logs import logs_bp  # noqa: F401, F811
    app.register_blueprint(logs_bp)

    from core.jobs import jobs_bp  # noqa: F401, F811
    app.register_blueprint(jobs_bp)

    from core.messages import messages_bp  # noqa: F401, F811
    app.register_blueprint(messages_bp)

    from core.files import files_bp  # noqa: F401, F811
    app.register_blueprint(files_bp)

    from core.nodes import nodes_bp  # noqa: F401, F811
    app.register_blueprint(nodes_bp)

    # import workspace blueprint and models
    from core.workspaces import workspaces_bp, models  # noqa: F401, F811
    app.register_blueprint(workspaces_bp)

    from api import api_bp  # noqa: F401, F811
    app.register_blueprint(api_bp)

    is_database_new = not database_exists(app.config['SQLALCHEMY_DATABASE_URI'])
    db.init_app(app)

    with app.app_context():
        db.create_all()

    if not minimal:
        migrate.init_app(app, db)
        jobManager.init_manager(app, db, config)
        workspaceManager.init_app(app, db)
        userManager.init_manager(app, db, workspaceManager, config)
        nodeManager.init_manager(app, db, workspaceManager)
        messageManager.init_manager(app, db, workspaceManager, config)
        menuBuilder.init_builder(app, db, userManager, workspaceManager)
        actionManager.init_manager(app, db, userManager, menuBuilder, workspaceManager, nodeManager, config)
        fileManager.init_manager(app, db, workspaceManager, config)

    with app.app_context():
        nodeManager.init_nodes()

    return app, is_database_new


# declare app routes
app_bp = Blueprint('app', __name__, static_folder="../client")

from core import routes  # noqa: F401
