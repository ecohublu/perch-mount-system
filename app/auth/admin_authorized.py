import flask_jwt_extended
import functools

from app.error_handler import errors

def admin_required():
    def wrapper(fn):
        @functools.wraps(fn)
        def decorator(*args, **kwargs):
            claims = flask_jwt_extended.get_jwt()
            if claims.get("is_admin"):
                return fn(*args, **kwargs)
            else:
                raise errors.Unauthorized(message="this is an admin only api")
        return decorator
    return wrapper


def super_admin_required():
    def wrapper(fn):
        @functools.wraps(fn)
        def decorator(*args, **kwargs):
            claims = flask_jwt_extended.get_jwt()
            if claims.get("is_super_admin"):
                return fn(*args, **kwargs)
            else:
                raise errors.Unauthorized(message="this is an super admin only api")
        return decorator
    return wrapper

