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

import os
import json
import configparser
from ast import literal_eval

basedir = os.path.abspath(os.path.dirname(__file__))


def remove_quotes(original):
    d = original.copy()
    for key, value in d.items():
        if isinstance(value, str):
            s = d[key]
            if s.startswith(('"', "'")):
                s = s[1:]
            if s.endswith(('"', "'")):
                s = s[:-1]
            d[key] = s
        if isinstance(value, dict):
            d[key] = remove_quotes(value)
    return d


class SystemConfigs:
    def __init__(self, preferences_ini):
        self.preferences_ini = preferences_ini

        self.config = configparser.ConfigParser()
        self.config.read(preferences_ini)

        self.d = self.to_dict(self.config._sections)

    def as_dict(self):
        return self.d

    def to_dict(self, config):
        """
        Nested OrderedDict to normal dict and remove quotes around string
        """
        d = json.loads(json.dumps(config))
        d = remove_quotes(d)
        return d


def load_config(file):
    def remove_quotes(data):
        d = data.copy()
        for key, value in d.items():
            if isinstance(value, str):
                s = d[key]
                if s.startswith(('"', "'")):
                    s = s[1:]
                    s = s[:-1]
                else:
                    s = literal_eval(s)
                d[key] = s
            if isinstance(value, dict):
                d[key] = remove_quotes(value)
        return d

    cfg_parser = configparser.ConfigParser()
    # add default sections
    cfg_parser.add_section("LDAP")
    cfg_parser.add_section("MAIL")
    cfg_parser.add_section("SYSTEM")
    cfg_parser.add_section("DEV")
    # read and overwrite
    cfg_parser.read(file)
    data = json.loads(json.dumps(cfg_parser._sections))
    config = remove_quotes(data)
    return config


def configure_app(app, config, test):
    # Configure application to store JWTs in cookies
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["CORS_HEADERS"] = "Content-Type"
    app.config["CORS_SUPPORTS_CREDENTIALS"] = True

    # Only allow JWT cookies to be sent over https. In production, this
    # should likely be True
    app.config["JWT_COOKIE_SECURE"] = False

    # Set the cookie paths, so that you are only sending your access token
    # cookie to the access endpoints, and only sending your refresh token
    # to the refresh endpoint. Technically this is optional, but it is in
    # your best interest to not send additional cookies in the request if
    # they aren't needed.
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/api/v1/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/api/v1/"

    database_path = config["SYSTEM"].get("database_path", None)
    if database_path is not None:
        database_path = "sqlite:///" + database_path

    if test:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            database_path or os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "test.db")
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            database_path or os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
        )

    # Enable csrf double submit protection. See this for a thorough
    # explanation: http://www.redotheweb.com/2015/11/09/api-security.html
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    # Set the secret key to sign the JWTs with
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["MAIL_SERVER"] = config["MAIL"].get("server", "server")
    app.config["MAIL_PORT"] = config["MAIL"].get("port", 465)
    app.config["MAIL_USERNAME"] = config["MAIL"].get("username", "username")
    app.config["MAIL_PASSWORD"] = config["MAIL"].get("password", "password")
    app.config["MAIL_USE_TLS"] = config["MAIL"].get("tls", False)
    app.config["MAIL_USE_SSL"] = config["MAIL"].get("ssl", True)
    app.config["MAIL_SENDER"] = config["MAIL"].get("sender", "")

    app.config["SYSTEM_ALLOW_BASIC_AUTH"] = config["DEV"].get("allow_basic_authentication", False)

    # app.config.from_pyfile('config.cfg', silent=True) # instance-folders configuration
