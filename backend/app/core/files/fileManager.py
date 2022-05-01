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
from core.logs import logManager


class FileManager(object):
    """ The FileManager ...
    """
    def __init__(self, ):
        # preparation to instanciate
        self.config = None
        self.app = None
        self.db = None
        self.workspaceManager = None

    def init_manager(self, app, db, workspaceManager, config):
        self.config = config
        self.app = app
        self.db = db
        self.workspaceManager = workspaceManager

        from core.files.models import FileStorage
        self.filestorage = FileStorage
        self.upload_dir_path = None

        if 'file_storage_path' in config['SYSTEM']:
            if os.path.exists(config['SYSTEM']['file_storage_path']):
                upload_dir_path = os.path.join(config['SYSTEM']['file_storage_path'], "uploads")
                if not os.path.exists(upload_dir_path):
                    os.mkdir(upload_dir_path)
                self.upload_dir_path = upload_dir_path
            else:
                logManager.error("FileManager 'file_storage_path' don't exist")
        else:
            logManager.error("FileManager attribute 'file_storage_path' not defined in config")

        logManager.info("FileManager initialized")
