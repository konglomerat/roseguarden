"""
The roseguarden project

Copyright (C) 2018-2021  Marcus Drobisch,

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

from datetime import time, timedelta
import arrow

from workspaces.Access.types import SpaceAccessType


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or arrow.utcnow().time()
    return check_time >= begin_time and check_time <= end_time


def needs_the_accesstype_a_budget(access_type: SpaceAccessType):
    if access_type is SpaceAccessType.UNLIMITED:
        return False
    else:
        return True


def do_accesstype_gets_recharge(access_type: SpaceAccessType):
    if access_type is SpaceAccessType.AUTO_RECHARGED_USER_BUDGET:
        return True
    else:
        return False


def do_accesstype_use_group_budget(access_type: SpaceAccessType):
    if access_type is SpaceAccessType.GROUP_BUDGET or access_type is SpaceAccessType.AUTO_RECHARGED_GROUP_BUDGET:
        return True
    else:
        return False


def update_user_access_properties_after_access_granted(user):
    access_group = user.spaceaccess_accessgroup
    access_properties = user.access
    if access_group is None:
        raise Exception("Unable to update access property for unassigned space access group")

    # check if user needs budget to access
    if access_group.access_need_budget:
        # decrement budget if last access is more than 24h ago
        budget_have_to_decrement = False
        if access_properties.last_access_at is None:
            budget_have_to_decrement = True
        elif arrow.utcnow() > (access_properties.last_access_at + timedelta(hours=24)):
            budget_have_to_decrement = True

        # if budget have to decrement update group or personal budget accordingly
        if budget_have_to_decrement:
            access_properties.last_access_at = arrow.utcnow()
            if access_group.access_use_group_budget:
                # update group access budget
                access_group.group_budget -= 1
            else:
                # update personal access budget
                access_properties.access_budget -= 1


def set_default_access_type_user_properties(user, access_type):
    pass


def is_user_budget_sufficient(user):
    access_group = user.spaceaccess_accessgroup
    access_properties = user.access
    if access_group is None:
        return False

    if access_group.access_type == SpaceAccessType.NO_ACCESS:
        return False

    # check if user needs budget to access
    if access_group.access_need_budget:
        if access_group.access_use_group_budget:
            # check group access budget
            if access_group.group_budget > 0:
                return True
            else:
                return False
        else:
            # check personal access budget
            if access_properties.access_budget > 0:
                return True
            else:
                return False

    else:
        return True


def has_user_access_to_space(user, node):

    if user.account_verified is False:
        return False, "User account not verified"

    if user.access is None:
        return False, "No access properties found for user"

    # check for users access start date
    if arrow.utcnow().date() < user.access.access_start_date.date():
        return False, "Access not started yet"

    # check for users access expiration
    if user.access.access_expires and arrow.utcnow().date() > user.access.access_expire_date.date():
        return False, "Access expired"

    # check for accessgroup assigned to user
    if user.spaceaccess_accessgroup is None:
        return False, "User is not in an access group"

    # check for node corresponding space assigned to accessgroup
    accessgroup = user.spaceaccess_accessgroup
    if len(accessgroup.spaces) == 0:
        return False, "No spaces mapped to this node"
    for s in accessgroup.spaces:
        if s not in user.spaceaccess_accessgroup.spaces:
            return False, "User has no access to the mapped space"

    # check for granted weekday
    if (accessgroup.day_access_mask & (1 << arrow.utcnow().date().weekday())) == 0:
        return False, "User has no access on this weekday"

    # check for granted daytime
    if not is_time_between(time(accessgroup.daily_access_start_time.hour, accessgroup.daily_access_start_time.minute),
                           time(accessgroup.daily_access_end_time.hour, accessgroup.daily_access_end_time.minute)):
        return False, "User has no access in this time range"

    return True, "Access granted"
