from core.users import userManager
from workspaces.Access.access import has_user_access_to_space


def test_verification_check(base_setup):
    """Test that an unverified user get access denied

    Uses the "unverified@fabba.space" user from the testEnv.py base environemnt.
    """
    u = userManager.getUser('unverified@fabba.space')
    access, message = has_user_access_to_space(u, None)
    assert access is False
