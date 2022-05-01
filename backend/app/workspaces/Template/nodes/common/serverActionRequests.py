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

from core.actions.actionGenerator import BaseNodeAction


class RequestPinAction(BaseNodeAction):
    action = 'requestPin'

    @classmethod
    def generate(cls, ):
        action = super(RequestPinAction, cls).generate()
        return action


class DenyAccessAction(BaseNodeAction):
    action = 'denyAccess'

    @classmethod
    def generate(cls, message, info, request_pin=False):
        action = super(DenyAccessAction, cls).generate()
        action['message'] = message
        action['info'] = info
        return action


class GrandAccessAction(BaseNodeAction):
    action = 'grandAccess'

    @classmethod
    def generate(cls, user):
        action = super(GrandAccessAction, cls).generate()
        if user is None:
            raise Exception("No user found")
        else:
            # add personal information
            info = "{} {}\n".format(user.firstname, user.lastname)
            action['message'] = "Welcome"
            action['info'] = info
        return action


class UpdateUserInfoAction(BaseNodeAction):
    action = 'updateUserInfo'

    @classmethod
    def generate(cls, user):
        action = super(UpdateUserInfoAction, cls).generate()
        if user is None:
            action['exist'] = False
            action['info'] = "Not found."
        else:
            # add personal information
            info = "{} {}\n".format(user.firstname, user.lastname)
            info = info + "{}\n".format(user.email)
            action['info'] = info
            action['exist'] = True
        return action


class UpdateAssignInfoAction(BaseNodeAction):
    action = 'updateAssignInfo'

    @classmethod
    def generate(cls, assign_key, assign_is_valid):
        action = super(UpdateAssignInfoAction, cls).generate()
        action['code'] = assign_key
        action['valid'] = assign_is_valid
        return action
