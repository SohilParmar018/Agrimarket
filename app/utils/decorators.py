"""
Custom decorators for access control
"""
from functools import wraps
from flask import abort
from flask_login import current_user


def farmer_required(f):
    """Require farmer role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_farmer():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def buyer_required(f):
    """Require buyer role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_buyer():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
