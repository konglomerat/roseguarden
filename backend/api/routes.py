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

from api import api_bp
from flask import request, make_response, current_app
from flask_jwt_extended import jwt_optional, get_jwt_identity, get_raw_jwt
from pprint import pprint
import json
from core import actionManager
from api.request import get_identity_by_basic_auth, get_expire_datetime_by_raw_jwt
import datetime


# this module routes the action based api on e.g. .../api/v1
# the api needs the generalized action based json-rpc form
# every app module can hold additional entrypoint in a rest based form
# e.g. '/login/refresh'


@api_bp.route("/api/v1", methods=["POST", "GET"])
@jwt_optional
def api_v1():
    print("call on api version v1")
    # pprint(request.json, indent=2)
    pprint(request.json, depth=2, indent=2)

    # try to get identity by jwt
    identity = get_jwt_identity()

    # if jwt not found try to get identity by basic auth
    if identity is None and current_app.config["SYSTEM_ALLOW_BASIC_AUTH"]:
        identity = get_identity_by_basic_auth(request)

    # try to get expire date for jwt auth
    expire_date = get_expire_datetime_by_raw_jwt(get_raw_jwt())

    # handle action
    reply = actionManager.handleActionRequest(identity, expire_date, request.json)
    print("Send reply:")
    pprint(reply, depth=2, indent=2)
    reply = json.dumps(reply)
    reply = make_response(reply, 200)
    return reply


"""     if get_jwt_identity() is not None:
        print("api call for ", request.method, " for valid user ", get_jwt_identity())
    else:
        print("api call for ", request.method, " for guest ")

    if request.method == "POST":
        logger.info("provide api response on post")
        logger.info(request.data)
        logger.info(request.args)
        argstr = ''
        for key, value in request.args.items():
            argstr += '"' + str(key) + '":' + ' "' + str(value) + '" '

        return "{ 'message': 'yeah', 'data': '" + str(request.data)  + "', 'args': '{" + argstr +  "}' }"
    else:
        logger.info("provide api response on get")
        return '{ "message": "hello world" }' """
