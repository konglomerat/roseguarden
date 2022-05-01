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
from core import app_bp
from flask import redirect, url_for, send_from_directory


# index route
@app_bp.route('/')
def index():
    return send_from_directory('../client', 'index.html')
    # return render_template("index.html")


@app_bp.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    if (os.path.isdir("./client/" + path)):
        return send_from_directory('../client/' + path, 'index.html')
    if (os.path.isfile("./client/" + path)):
        return app_bp.send_static_file(path)
    else:
        return send_from_directory('../client/section', 'index.html')


@app_bp.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
