from enum import Enum


class UserRole(Enum):
    admin = "admin"
    user = "user"

class UserStatus(Enum):
    active = "active"
    inactive = "inactive"