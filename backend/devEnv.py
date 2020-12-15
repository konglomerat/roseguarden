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
__contact__ =  "roseguarden@fabba.space"
__credits__ = []
__license__ = "GPLv3"

import os
from pprint import pprint
from core.users.models import User
from core.messages.models import Message
from core.workspaces.models import Permission, PermissionGroup
from core.messages import send_mail, send_message
from core.jobs import jobManager, add_dated_job
from core.workspaces import workspaceManager
from core.actions import generateActionLink
from core.actions.models import ActionLink
from core.logs import logManager
from core.users import userManager
from core.nodes.nodeClass import NodeClass
import arrow
import pprint
import json

from workspaces.Log.permissions import ViewLogs
from workspaces.Access.models import SpaceAccessGroup, SpaceAccessProperties, SpaceAccessSpace
from workspaces.Template.nodes.nodeTemplate import NodeTemplate

from core.workspaces.workspaceHooks import WorkspaceHooks
from core.nodes import nodeManager
from core.nodes.models import Node

from core.actions import models
from core.files import models
from core.jobs import models
from core.messages import models
from core.workspaces import models
from core.users import models
from core.nodes import models

def create_devEnv(app, db, clean=True):
    print()
    print("Create dev enviroment")
    if clean is True:
        PermissionGroup.query.delete()
        SpaceAccessGroup.query.delete()
        SpaceAccessSpace.query.delete()
        ActionLink.query.delete()

    pAll = Permission.query.all()
    permissions = {}
    print('Detected permissions:')
    for p in pAll:
        permissions[p.name] = p

    pg = PermissionGroup(name= 'Supervisor')
    if 'Log.ViewLogs' in permissions:
        pg.permissions.append(permissions['Log.ViewLogs'])
    db.session.add(pg)

    u = User.query.filter_by(email='roseguarden@fabba.space').first()
    if u is None:
        u = User(email='roseguarden@fabba.space', password='test1234', isAdmin=False)
        u.firstname = "Test"
        u.lastname = "User"
        u.organization = "Konglomerat"
        u.account_verified = True
        u.pin = "222222"
        workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=u)
        db.session.add(u)

    s = User.query.filter_by(email='super@fabba.space').first()
    if s is None:
        s = User(email='super@fabba.space', password='test1234', isAdmin=False)
        s.firstname = "Super"
        s.lastname = "User"
        s.organization = "Konglomerat"
        s.account_verified = True
        s.pin = "111111"
        s.permission_groups.append(pg)
        workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=s)
        db.session.add(s)

    a = User.query.filter_by(email='admin@fabba.space').first()
    if a is None:
        a = User(email='admin@fabba.space', password='admin1234', isAdmin=True)
        a.firstname = "Test"
        a.lastname = "Admin"
        a.organization = "Konglomerat"
        a.account_verified = True
        a.pin = "123456"
        workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=a)
        db.session.add(a)

    node_ident =     {
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
        nodeManager.create_node_from_identification(node_ident,node_fingerprint, node_authentification)
        nodeManager.authorizeNode(node_fingerprint)

    sas = SpaceAccessSpace(name="Garage workshop")
    sas.description = "The garage workshop"
    sas.entrance_node = [n]
    db.session.add(sas)

    ag = SpaceAccessGroup(name="Friends (full access)")
    ag.spaces.append(sas)

    s = User.query.filter_by(email='super@fabba.space').first()
    if s is not None:
        ag.users.append(s)
    if a is not None:
        ag.users.append(a)
    
    ag.note = "Friends with full access"
    ag.access_type = 'Unlimited'
    ag.daily_access_start_time = arrow.get('00:00', 'HH:mm')
    ag.daily_access_end_time = arrow.get('23:59', 'HH:mm')
    ag.door_access_mask = 3
    ag.day_access_mask = 127
    ag.access_expires_as_default = False
    ag.access_expires_default_days = 365   
    db.session.add(ag)

    #p = Permission(user=s, name= ViewLogs)
    pAll = Permission.query.all()
    print(pAll)



    usersWorkspace = workspaceManager.getWorkspace('Users')
    data = {
        'username' : 'mdrobisch'
    }
    #send_mail(["m.drobisch@googlemail.com"], "Welcome", usersWorkspace, 'welcome.mail', data )
    #send_message(u, "Welcome", usersWorkspace, 'welcome.message', data, 'Roseguarden')
    #send_message(s, "Welcome", usersWorkspace, 'welcome.message', data, 'Roseguarden')
    #send_message(a, "Welcome", usersWorkspace, 'welcome.message', data, 'Roseguarden')
    #print(generateActionLink(usersWorkspace, 'verifyUser', { 'email' : "roseguarden@fabba.space" }, "dashboard"))

    db.session.commit()

   # userManager.removeUser('roseguarden@fabba.space')

    all_user = User.query.all()
    print(all_user)
    for user in all_user:        
        print(f' User: {user} {user.password} ')

    print("n")

    print(jobManager)
    args = ["test"]
    # add_dated_job("UpdateBudgetsWeeklyJob", args, workspace="Access" )
    
    mAll = Message.query.all()
