import time
from core.users import userManager
from core.users.enum import UserAuthenticatorStatus
from core.workspaces import workspaceManager
from core.workspaces.workspaceHooks import WorkspaceHooks

import pytest

from core.users.models import User


@pytest.fixture(scope="function")
def high_user_count(base_setup):
    app, app_context, db, client = base_setup
    all_user = User.query.all()
    for x in range(30):
        email = f'test{x}@fabba.space'
        # check if user already exist in the db
        user_list = []
        if len([u for u in all_user if u.email == email]) == 0:
            authenticator_private_key = f"0.0.0.0.{x}"
            authenticator_public_key = ""

            u = User(email=email, password='test1234', isAdmin=False)
            u.firstname = "Test"
            u.lastname = "User"
            u.organization = "Konglomerat"
            u.account_verified = True
            u.pin = "123456"
            u.authenticator = authenticator_private_key
            u.authenticator_public_key = userManager.getAuthenticatorPublicKeyOrDefault(authenticator_private_key, 
                                                                                        authenticator_public_key)
            u.authenticator_status = UserAuthenticatorStatus.VALID
            workspaceManager.triggerWorkspaceHooks(WorkspaceHooks.CREATEUSER, user=u)
            user_list.append(u)
        db.session.bulk_save_objects(user_list)
    db.session.commit()


def test_get_user_by_authenticator_performance_for_not_exisiting_authenticator(high_user_count):
    """Check the performance for a not exisiting authenticator

    The test try to get a the user for the a authenticator that is not available.

    """

    before = time.time()
    # search for an nonexisitng authenticator
    u = userManager.get_user_by_authenticator("99.99.99.99.99", "")
    after = time.time()
    # no user should be found
    assert u is None
    elapsed_in_seconds = after - before
    print(elapsed_in_seconds)
    # get_user_by_authenticator have to run in 2 seconds
    assert elapsed_in_seconds <= 2.0


def test_get_user_by_authenticator_performance(high_user_count):
    """Check the performance for a exisiting authenticator

    The test check for an authenticator of the last users available in the high_user_count test environemt.

    """

    before = time.time()
    # search for an exisitng authenticator
    u = userManager.get_user_by_authenticator("0.0.0.0.29", "")
    after = time.time()
    # no user should be found
    assert u is not None
    elapsed_in_seconds = after - before
    print(elapsed_in_seconds)
    # get_user_by_authenticator have to run in 2 seconds
    assert elapsed_in_seconds <= 2.0
