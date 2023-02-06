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

from workspaces.Access.types import SpaceAccessType


def get_accessable_spaces_for_user_string(space_access_group):
    spaces_string = ""
    for s in space_access_group.spaces:
        if spaces_string != "":
            spaces_string += ", "
        spaces_string += s.name
    if spaces_string == "":
        spaces_string = "None"
    return spaces_string


def get_user_accessable_weekdays_string(space_access_group):
    weekday_string = ""
    if space_access_group.day_access_mask & 0x01:
        if weekday_string != "":
            weekday_string += ", "
        weekday_string += "Mon."
    if space_access_group.day_access_mask & 0x02:
        if weekday_string != "":
            weekday_string += ", "
        weekday_string += "Tue."
    if space_access_group.day_access_mask & 0x04:
        if weekday_string != "":
            weekday_string += ", "
        weekday_string += "Wed."
    if space_access_group.day_access_mask & 0x08:
        if weekday_string != "":
            weekday_string += ", "
        weekday_string += "Thu."
    if space_access_group.day_access_mask & 0x10:
        if weekday_string != "":
            weekday_string += ", "
        weekday_string += "Fri."
    if space_access_group.day_access_mask & 0x20:
        if weekday_string != "":
            weekday_string += ", "
        weekday_string += "Sat."
    if space_access_group.day_access_mask & 0x40:
        if weekday_string != "":
            weekday_string += ", "
        weekday_string += "Sun."
    if weekday_string == "":
        weekday_string = "None"
    return weekday_string


def get_access_budget_short_string(user_space_access_group, user_space_access_properties):
    if user_space_access_group.access_type is SpaceAccessType.NO_ACCESS:
        return "No access at the moment."
    if user_space_access_group.access_type is SpaceAccessType.UNLIMITED:
        return "Unlimited days of access."
    if user_space_access_group.access_type is SpaceAccessType.USER_BUDGET:
        return f"{user_space_access_properties.access_budget} days of access left."
    if user_space_access_group.access_type is SpaceAccessType.GROUP_BUDGET:
        return f"{user_space_access_group.group_budget} days of access left."
    if user_space_access_group.access_type is SpaceAccessType.AUTO_RECHARGED_USER_BUDGET:
        return (
            f"{user_space_access_properties.access_budget} of "
            f"{user_space_access_group.access_recharge_budget_amount} days of access left."
        )

    if user_space_access_group.access_type is SpaceAccessType.AUTO_RECHARGED_GROUP_BUDGET:
        return (
            f"{user_space_access_group.group_budget} of "
            f"{user_space_access_group.access_recharge_budget_amount} days of access left."
        )


def get_access_info_string(user_space_access_group, user_space_access_properties):
    if user_space_access_group.access_type is SpaceAccessType.NO_ACCESS:
        return "You don't have access at the moment"
    if user_space_access_group.access_type is SpaceAccessType.UNLIMITED:
        return f"You have access on unlimited {user_space_access_group.entry_accounting_type.value}"
    if user_space_access_group.access_type is SpaceAccessType.USER_BUDGET:
        return (
            f"You have a personal budget of {user_space_access_properties.access_budget} "
            f"{user_space_access_group.entry_accounting_type.value} access."
        )
    if user_space_access_group.access_type is SpaceAccessType.GROUP_BUDGET:
        return (
            f"You have a group budget of {user_space_access_group.group_budget} "
            f"{user_space_access_group.entry_accounting_type.value} access."
            f"within your group '{user_space_access_group.name}'"
        )
    if user_space_access_group.access_type is SpaceAccessType.AUTO_RECHARGED_USER_BUDGET:
        return (
            f"You have a personal budget of {user_space_access_properties.access_budget} "
            f"{user_space_access_group.entry_accounting_type.value}. "
            f"You get recharged with {user_space_access_group.access_recharge_budget_amount} "
            f" new {user_space_access_group.entry_accounting_type.value} access "
            f"after every {user_space_access_group.access_recharge_budget_every_periods} "
            f"{user_space_access_group.access_recharge_budget_period.value.lower()}"
        )
    if user_space_access_group.access_type is SpaceAccessType.AUTO_RECHARGED_GROUP_BUDGET:
        return (
            f"You have a group budget of {user_space_access_group.group_budget} "
            f"{user_space_access_group.entry_accounting_type.value} access "
            f"within your group '{user_space_access_group.name}'. "
            f"You get recharged with {user_space_access_group.access_recharge_budget_amount} "
            f" new {user_space_access_group.entry_accounting_type.value} access "
            f"after every {user_space_access_group.access_recharge_budget_every_periods} "
            f"{user_space_access_group.access_recharge_budget_period.value.lower()}"
        )

    return user_space_access_group.access_type.value
