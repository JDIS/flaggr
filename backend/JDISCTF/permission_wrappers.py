"""
Set of function wrappers for managing API permissions (account type, roles, etc.)
"""
import functools

from flask_login import current_user
from flask_rebar import errors

from JDISCTF.models import Administrator, Event


def require_participant(func):
    """
    Ensures that the current user is a participant account and
    injects the corresponding Participant as kwarg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        current_participant = current_user.get_participant()
        if current_participant is None:
            raise errors.Unauthorized("You must be a participant to access this resource.")

        kwargs['current_participant'] = current_participant
        return func(*args, **kwargs)

    return wrapper


def validate_and_get_current_admin_for_event(event_id: int):
    """
    :param event_id: The event id for validation
    :return: The current admin for the specified event if it can administer it.
    """
    current_admin: Administrator = current_user.get_administrator()
    if current_admin is None:
        raise errors.Unauthorized("You must be an administrator to access this resource.")
    if event_id not in map(lambda x: x.id, current_admin.events):
        raise errors.Unauthorized("You do not have the permission to administer this event.")
    return current_admin


def require_admin_for_event(func, event_id: int):
    """
    Ensures that the current user is an administrator account for the given event
    and injects the corresponding Administrator as kwarg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['current_admin'] = validate_and_get_current_admin_for_event(event_id)
        return func(*args, **kwargs)

    return wrapper


def require_admin_with_role(func, event_id: int, role: str):
    """
    Ensures that the current user is an administrator account with the required role.
    Injects the corresponding Administrator as kwarg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        current_admin = validate_and_get_current_admin_for_event(event_id)
        if role not in current_admin.get_roles_for_event(event_id):
            raise errors.Unauthorized("You do not have the required role"
                                      "to perform this action.")

        kwargs['current_admin'] = current_admin
        return func(*args, **kwargs)

    return wrapper


def require_admin(func):
    """
    Ensures that the current user is an administrator account
    and injects the corresponding Administrator as kwarg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        current_admin: Administrator = current_user.get_administrator()
        if current_admin is None:
            raise errors.Unauthorized("You must be an administrator to access this resource.")

        kwargs['current_admin'] = current_admin
        return func(*args, **kwargs)

    return wrapper


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
