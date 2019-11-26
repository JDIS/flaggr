"""
Set of function wrappers for managing API permissions (account type, roles, etc.)
"""
import functools

from flask_login import current_user
from flask_rebar import errors


def require_participant(func):
    """Ensures that the current user is a participant account and injects the corresponding Participant as kwarg"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        current_participant = current_user.get_participant()
        if current_participant is None:
            raise errors.Unauthorized("You must be a participant to access this resource.")

        kwargs['current_participant'] = current_participant
        return func(*args, **kwargs)

    return wrapper
