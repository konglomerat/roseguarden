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


class MenuBuilder(object):
    """ The MenuBuilder ...
    """
    def __init__(self, ):
        # preparation to instanciate
        self.actionsMap = {}

    def init_builder(self, app, db, userManager, workspaceManager):
        self.app = app
        self.db = db
        self.workspaceManager = workspaceManager
        self.userManager = userManager

    def makeHeader(self, name):
        header = {}
        header['header'] = name
        return header

    def makeDivider(self, ):
        divider = {}
        divider['divider'] = True
        return divider

    def makeEntry(self, title, group, name, icon, path, external=False):
        entry = {}
        entry['title'] = title
        entry['group'] = group
        entry['name'] = name
        entry['icon'] = icon
        entry['href'] = path
        entry['external'] = external
        return entry

    def buildGuestMenu(self, ):
        print("buildGuestMenu")
        menu = []
        menu.append(self.makeHeader('Roseguarden'))
        menu.append(self.makeEntry('Home', 'app', 'Dashboard', 'dashboard', '/dashboard'))
        menu.append(self.makeDivider())
        return menu

    def buildUserMenu(self, user):
        print("buildUserMenu")
        menu = self.buildGuestMenu()
        menu.append(self.makeHeader('User'))
        menu.append(self.makeEntry(title='Account', group='user', name='Account', icon='face', path='/user/account'))
        menu.append(self.makeDivider())
        return menu

    def buildAdminMenu(self, user):
        print("buildAdminMenu")
        menu = self.buildUserMenu(user)
        menu.append(self.makeHeader('Admin'))
        menu.append(self.makeEntry('Users', 'admin', 'Users', 'supervisor_account', '/admin/users'))
        menu.append(self.makeEntry('Permissions', 'admin', 'Permissions', 'verified_user', '/admin/permissions'))
        # menu.append(self.makeEntry('Access cards'   , 'admin', 'Cards'       , 'credit_card', '/admin/cards'))
        # menu.append(self.makeEntry('Space access'   , 'admin', 'Access'      , 'lock', '/admin/access'))
        # menu.append(self.makeEntry('Nodes'          , 'admin', 'Nodes'       , 'adjust', '/admin/nodes'))
        menu.append(self.makeEntry('Log', 'admin', 'Log', 'description', '/admin/log'))

        menu.append(self.makeDivider())
        return menu

    def checkUserPermissions(self, user, requirement, workspace):
        key = workspace.name + '.' + requirement.name
        for g in user.permission_groups:
            for p in g.permissions:
                if key == p.name:
                    return True
        return False

    def hasPermission(self, user, page, workspace):
        if user is None:
            if page.requireLogin is False:
                return True
        else:
            if user.admin is True:
                return True
            if page.requireAdmin is False:
                if hasattr(page, 'requirePermission'):
                    if page.requirePermission is None:
                        return True
                    else:
                        return self.checkUserPermissions(user, page.requirePermission, workspace)
        return False

    def buildMenu(self, user):
        menu_groups = {}
        for w in self.workspaceManager.workspaces:
            for key, p in w.pages.items():
                # is pages in a group
                if p.group is not None:
                    if str(p.group) in menu_groups:
                        rankSum, pageList = menu_groups[str(p.group)]

                        if self.hasPermission(user, p, w):
                            pageList.append(p)

                        pageList.sort(key=lambda x: x.rank, reverse=True)
                        menu_groups[str(p.group)] = rankSum + p.rank, pageList
                    else:
                        if self.hasPermission(user, p, w):
                            menu_groups[str(p.group)] = p.rank, [p]
                        else:
                            menu_groups[str(p.group)] = p.rank, []
                else:
                    if self.hasPermission(user, p, w):
                        menu_groups['_' + str(p.name)] = p.rank, [p]

        sorted_menu_groups = sorted(menu_groups.items(), key=lambda x: x[1], reverse=True)

        menu = []
        for key, element in enumerate(sorted_menu_groups):
            group, (rank, pagelist) = element
            if len(pagelist) > 0:
                menu.append(self.makeHeader(str(group)))
                for p in pagelist:
                    print(p)
                    menu.append(self.makeEntry(title=p.title, group=p.group, name=p.name, icon=p.icon, path=p.route))
                menu.append(self.makeDivider())
        if len(menu) > 0:
            menu.pop()

        return menu


'''
EXAMPLE of menu structure
[
  {header: 'roseguarden'},
  {
    title: 'Home',
    group: 'apps',
    icon: 'dashboard',
    name: 'Dashboard',
    href: 'dashboard'
  },
  {divider: true},
  {header: 'Templates&Links'},
  {
    title: 'Vue Material Admin',
    group: 'links',
    icon: 'touch_app',
    external: true,
    href: 'https://github.com/tookit/vue-material-admin'
  },
  {
    title: 'Vue Material Admin Demo',
    group: 'links',
    icon: 'touch_app',
    external: true,
    href: 'http://vma.isocked.com/#/dashboard'
  },
  {
    title: 'Vuetify',
    group: 'links',
    icon: 'touch_app',
    external: true,
    href: 'https://vuetifyjs.com/en/getting-started/quick-start'
  }
];

'''
