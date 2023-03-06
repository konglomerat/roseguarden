import datetime
from core import userManager


def get_identity_by_basic_auth(request):
    if request.authorization is None:
        return None
    else:
        username = request.authorization.get("username", None)
        password = request.authorization.get("password", "")
        user = userManager.getUser(username)
        if user is not None and password != "" and user.checkPassword(password):
            return username


def get_expire_datetime_by_raw_jwt(raw_jwt):
    if "exp" in raw_jwt:
        return datetime.datetime.fromtimestamp(raw_jwt["exp"])
    else:
        return None
