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

from core.users.models import User
from core.users.enum import UserAuthenticatorStatus
from core.workspaces.models import Permission, PermissionGroup
from core.messages import send_message
from core.jobs import jobManager
from core.workspaces import workspaceManager
from core.actions.models import ActionLink
import arrow

from workspaces.Access.models import SpaceAccessGroup, SpaceAccessSpace, AccessgroupSpaceMap, SpaceNodeMap
from workspaces.Access.types import SpaceAccessType
from core.workspaces.workspaceHooks import WorkspaceHooks
from core.nodes import nodeManager
from core.nodes.models import Node

import core.actions.models  # noqa: F401
import core.files.models  # noqa: F401
import core.jobs.models  # noqa: F401
import core.messages.models  # noqa: F401
import core.workspaces.models  # noqa: F401


def create_devEnv(app, db, clean=True):
    print()
    print("Create dev enviroment")
    if clean is True:
        PermissionGroup.query.delete()
        AccessgroupSpaceMap.query.delete()
        SpaceAccessGroup.query.delete()
        SpaceAccessSpace.query.delete()
        SpaceNodeMap.query.delete()
        ActionLink.query.delete()

    pAll = Permission.query.all()
    permissions = {}
    print('Detected permissions:')
    for p in pAll:
        permissions[p.name] = p

    pg = PermissionGroup(name='Supervisor')
    if 'Log.ViewLogs' in permissions:
        pg.permissions.append(permissions['Log.ViewLogs'])
    db.session.add(pg)

    usersWorkspace = workspaceManager.getWorkspace('Users')

    u = User.query.filter_by(email='roseguarden@fabba.space').first()
    if u is None:
        u = User(email='roseguarden@fabba.space', password='test1234', isAdmin=False)
        u.firstname = "Test"
        u.lastname = "User"
        u.organization = "Konglomerat"
        u.account_verified = True
        u.pin = "123456"
        workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=u)
        db.session.add(u)
        data = {'username': u.firstname + " " + u.lastname}
        send_message(u, "Welcome", usersWorkspace, 'welcome.message', data, 'Roseguarden')

    s = User.query.filter_by(email='super@fabba.space').first()
    if s is None:
        s = User(email='super@fabba.space', password='test1234', isAdmin=False)
        s.firstname = "Super"
        s.lastname = "User"
        s.organization = "Konglomerat"
        s.account_verified = True
        s.pin = "123456"
        s.permission_groups.append(pg)
        workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=s)
        db.session.add(s)
        data = {'username': s.firstname + " " + s.lastname}
        send_message(s, "Welcome", usersWorkspace, 'welcome.message', data, 'Roseguarden')

    a = User.query.filter_by(email='admin@fabba.space').first()
    if a is None:
        a = User(email='admin@fabba.space', password='admin1234', isAdmin=True)
        a.firstname = "Test"
        a.lastname = "Admin"
        a.organization = "Konglomerat"
        a.account_verified = True
        a.pin = "123456"
        a.setAuthenticatorHash(b'$2b$12$zOn/sn5hpG02xpwvj74zruGHBGYCDgayBacy9Q9zBgM6.OEExh5Zm')
        a.authenticator_status = UserAuthenticatorStatus.VALID
        workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=a)
        db.session.add(a)
        data = {'username': a.firstname + " " + a.lastname}
        send_message(a, "Welcome", usersWorkspace, 'welcome.message', data, 'Roseguarden')

    uva = User.query.filter_by(email='unverified@fabba.space').first()
    if uva is None:
        uva = User(email='unverified@fabba.space', password='test1234', isAdmin=True)
        uva.firstname = "Test"
        uva.lastname = "Unverifed"
        uva.organization = "Konglomerat"
        uva.account_verified = False
        uva.pin = "123456"
        workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=uva)
        db.session.add(uva)
        data = {'username': uva.firstname + " " + uva.lastname}
        send_message(uva, "Welcome", usersWorkspace, 'welcome.message', data, 'Roseguarden')

    node_ident = {
        "nodename": "Door 1",
        "classname": "Door",
        "classworkspace": "Access",
        "classid": "00:01:AB:EF:19:D8:00:11",
        "firmware_version": "0.1.2",
        "firmware_compiled_at": "2007-12-22T18:21:01",
        "firmware_flashed_at": "2007-12-24T11:31:02",
        "hardware_version": "0.1.0"
    }
    node_fingerprint = "43:51:43:A1:B5:FC:8B:B7:0A:3A:A9:B1:0F:66:73:A8:73:A8:19:B1"
    node_authentification = "Kol-Bi-Hop-Ban-Gan-To-Sep+129"

    n = Node.query.filter_by(fingerprint=node_fingerprint).first()
    if n is None:
        nodeManager.create_node_from_identification(node_ident, node_fingerprint, node_authentification)
        nodeManager.authorizeNode(node_fingerprint)
        n = Node.query.filter_by(fingerprint=node_fingerprint).first()

    sas = SpaceAccessSpace(name="Garage workshop")
    sas.description = "The garage workshop"
    sas.entrance_nodes = [n]
    db.session.add(sas)

    ag = SpaceAccessGroup(name="Friends (full access)")
    ag.spaces = [sas]

    s = User.query.filter_by(email='super@fabba.space').first()
    if s is not None:
        ag.users.append(s)
    if a is not None:
        ag.users.append(a)

    ag.note = "Friends with full access"
    ag.access_type = SpaceAccessType.UNLIMITED
    ag.daily_access_start_time = arrow.get('00:00', 'HH:mm')
    ag.daily_access_end_time = arrow.get('23:59', 'HH:mm')
    ag.door_access_mask = 3
    ag.day_access_mask = 127
    ag.access_expires_as_default = False
    ag.access_expires_default_days = 365
    db.session.add(ag)

    # p = Permission(user=s, name= ViewLogs)
    pAll = Permission.query.all()
    print(pAll)

    # send_mail(["m.drobisch@googlemail.com"], "Welcome", usersWorkspace, 'welcome.mail', data )
    # print(generateActionLink(usersWorkspace, 'verifyUser', { 'email' : "roseguarden@fabba.space" }, "dashboard"))

    db.session.commit()

    # userManager.removeUser('roseguarden@fabba.space')

    all_user = User.query.all()
    print(all_user)
    for user in all_user:
        print(f' User: {user} {user.password} ')

    print("n")

    print(jobManager)
