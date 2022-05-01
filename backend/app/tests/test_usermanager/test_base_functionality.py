import time
from core.users import userManager
from core.users.enum import UserAuthenticatorStatus
from core.workspaces import workspaceManager
from core.workspaces.workspaceHooks import WorkspaceHooks

import pytest

from core.users.models import User


def test_public_authenticator_gets_set_to_default(base_setup):
    """Test that an empty authenticator will set to default automatically

    Uses the "roseguarden@fabba.space" user from the devEnv.py base environemnt.
    """
    u = userManager.get_user_by_authenticator("111.222.333.000", "")
    assert u is not None
    assert u.authenticator_public_key != ""

