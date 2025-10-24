from flask import g
from db import db
from application.models.users import UserModel

def role_checker(required_role):
    def decorator(f):
        def wrapper(*args, **kwargs):
            user_admin = db.session.query(UserModel).filter_by(user_id = g.user_id).first()
            user_role = user_admin.role.value
            if user_role != required_role:
                return {"message": "Access Denied", "success": False}, 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
