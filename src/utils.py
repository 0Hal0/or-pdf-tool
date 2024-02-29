from functools import wraps
from flask import current_app
from .models import UserTypes

def import_user():
    try:
        from flask_login import current_user
        return current_user
    except ImportError as exc:
        raise ImportError(
            "User argument not passed and Flask-Login current_user could not be imported"
        ) from exc

def admin_required(get_user=import_user):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_user = get_user()
            if current_user.userType == UserTypes.admin:
                return func(*args, **kwargs)
            return current_app.login_manager.unauthorized()
        return inner
    return wrapper

def is_admin(user):
    return user.userType == UserTypes.admin