from core.workspaces.page import Page
""" The startpage
"""


class Startpage(Page):
    title = 'Home'  # Shown label of the page in the menu
    group = 'Roseguarden'  # groupname multiple pages
    icon = 'dashboard'  # icon (in typeset of material design icons)
    route = '/dashboard'  # routing
    builder = 'frontend'  # page get build by the client (frontend)
    rank = 1000.0  # ranks (double) the page higher values are at the top of the menu
    # groups will be ranked by the sum of the rank-values of their entries
    startpage = True  # will define if the page is the startpage or not, their can only be one startpage
    requireLogin = False  # login is required to view the page
    requireAdmin = False  # login dont need admin privileges
    requirePermission = None  # No permission is rewuired to view the page, the value have to be defined
    # can be None, Permission or a list of Permissions
