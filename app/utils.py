from flask import abort
from flask_login import current_user
from functools import wraps

def role_required(role_id):
    """
    Decorator to restrict access based on role ID.
    :param role_id: Minimum role ID required for access
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role_id>role_id:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator