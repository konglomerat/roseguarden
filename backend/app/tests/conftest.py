import pytest

from core import create_app, db
from testEnv import create_testEnv


@pytest.fixture(scope="session")
def base_setup():
    """
    This function prepares and destruct the flask application and the database
    before and after each test.
    All lines before the yield statement will be executed before the tests
    and each line after the yield statement will be called at the end of the tests
    """
    app, _ = create_app(config_file="config_test.ini", test=True)
    app_context = app.app_context()
    app_context.push()
    create_testEnv(app, db)
    client = app.test_client()

    yield app, app_context, db, client

    db.session.remove()
    db.drop_all()
    app_context.pop()
