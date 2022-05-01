from enum import Enum


class UserAuthenticatorStatus(Enum):
    UNSET = "Unset"
    LOCKED = "Locked"
    VALID = "Valid"


class AuthenticatorValidityType(Enum):
    ONCE = "Once"
    LIMITED_USAGE = "Limited"
    EXPIRATION_DATE = "Expires"


class AuthenticatorType(Enum):
    USER = "User"
    GUEST = "Guest"
    LOGIN = "Login"
    ACTION = "Action"


class AuthenticatorSendBy(Enum):
    MAIL = "Mail"
    NODE = "Node display"
    CLIENT = "Client"
    PHONE = "Phone"
