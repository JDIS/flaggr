"""
Set of function wrappers for managing API permissions (account type, roles, etc.)
"""
import functools

from flask_login import current_user
from flask_rebar import errors

from JDISCTF.models import Event


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
