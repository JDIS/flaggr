"""
Set of function wrappers for managing API permissions (account type, roles, etc.)
"""
import functools

from flask_login import current_user
from flask_rebar import errors

from JDISCTF.models import Administrator, Event


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


def require_admin(event_id: int):
    """Ensures that the current user is an administrator account and injects the corresponding Administrator as kwarg"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_admin: Administrator = current_user.get_administrator()
            if current_admin is None:
                raise errors.Unauthorized("You must be an administrator to access this resource.")

            if event_id not in map(lambda x: x.id, current_admin.events):
                raise errors.Unauthorized("You do not have the permission to administer this event.")

            kwargs['current_admin'] = current_admin
            return func(*args, **kwargs)

        return wrapper
    return decorator


def require_admin_with_role(event_id: int, role: str):
    """
    Ensures that the current user is an administrator account with the required role.
    Injects the corresponding Administrator as kwarg
    """
    @require_admin(event_id)
    def decorator(func, current_admin: Administrator):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if role not in current_admin.get_roles_for_event(event_id):
                raise errors.Unauthorized("You do not have the required role to perform this action.")

            kwargs['current_admin'] = current_admin
            return func(*args, **kwargs)

        return wrapper
    return decorator


def require_event(func):
    """
    Decorator that fetches the current event by parsing the URL. Requires an 'event_id' int
    in the request, or a 400 Bad Request is returned.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'event_id' not in kwargs:
            raise errors.BadRequest('The request requires an event ID')
        event = Event.query.filter_by(id=kwargs['event_id']).first()
        if event is None:
            raise errors.NotFound(f"Event with ID {kwargs['event_id']} not found.")

        kwargs['event'] = event
        del kwargs['event_id']
        return func(*args, **kwargs)

    return wrapper
