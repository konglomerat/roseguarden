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

from core.files import files_bp
from flask import request
from werkzeug import secure_filename
import os

from . import fileManager


@files_bp.route('/api/v1/file/download/<id>', methods=['GET'])
def file_request(id):
    return "File", 200


@files_bp.route('/api/v1/file/upload', methods=['POST'])
def upload_request():
    print(request.files)
    for f in request.files.values():
        print(secure_filename(f.filename))
        if fileManager.upload_dir_path is not None:
            f.save(os.path.join(fileManager.upload_dir_path, secure_filename(f.filename)))
        else:
            return 'file uploaded failed', 500

    return 'file uploaded successfully', 200
