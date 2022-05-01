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


class Action(object):
    """Base class that each action for every workspace have to inherit from.
       The class define methods that all action must implement by the plugin
    """

    disable = False

    def __init__(self, app, uri=None):
        if uri is None:
            self.uri = self.__class__.__name__
        else:
            self.uri = uri

    def handle(self, action, user, workspace, actionManager):
        """ Action handler method
        """
        raise NotImplementedError

    @staticmethod
    def generate(**kwargs):
        """ Action generator method
        """
        raise NotImplementedError
