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

from core.nodes import nodes_bp, nodeManager
from core.nodes.errors import AuthorizationError, RequestError
from core.logs import logManager
from flask import make_response, request
from flask_cors import cross_origin
from pprint import pprint
import json


@cross_origin()
@nodes_bp.route('/api/v1/nodes', methods=["POST"])
def nodes():
    reply_dict = {}
    s = json.dumps(request.json, indent=4)
    logManager.info("node request from: {}:\n{}".format(request.remote_addr, s))
    if request.method == "OPTIONS":
        return make_response("", 200)

    if request.json is not None:
        try:
            reply_dict = nodeManager.handle_node_request(request.json)
        except AuthorizationError as ae:
            return make_response(str(ae), 401)
        except RequestError as re:
            return make_response(str(re), 400)

        reply = json.dumps(reply_dict)
        pprint(reply)
        return make_response(reply, 200)
    else:
        return make_response("No json data", 400)


@nodes_bp.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    return response
