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

from app.workspaces import DataView, Workspace, Page
from app.users.models import User
from app import db

""" The log page
"""
class AuthenticatorList(Page):
    title = 'Authenticator'              # Shown label of the page in the menu
    group = 'Admin'       # groupname multiple pages 
    icon = 'credit_card'          # icon (in typeset of material design icons)
    route = '/admin/authenticator'            # routing 
    builder = 'frontend'        # page get build by the client (frontend)
    rank = 1.6               # ranks (double) the page higher values are at the top of the menu
                                # groups will be ranked by the sum of the rank-values of their entries 
    requireLogin = True        # login is required to view the page