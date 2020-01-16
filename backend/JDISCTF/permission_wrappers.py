"""
Set of function wrappers for managing API permissions (account type, roles, etc.)
"""
import functools

from flask_login import current_user
from flask_rebar import errors

from JDISCTF.models import Administrator, Challenge, Event


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
    wrapper.func = func  # To bypass decorator in unit testing
    return wrapper


def validate_and_get_current_admin_for_event(event_id: int):
    """
    :param event_id: The event id for validation
    :return: The current admin for the specified event if it can administer it.
    """
    current_admin: Administrator = current_user.get_administrator()
    if current_admin is None:
        raise errors.Unauthorized("You must be an administrator to access this resource.")
    if not current_admin.is_admin_of_event(event_id):
        raise errors.Unauthorized("You do not have the permission to administer this event.")
    return current_admin


# Maybe this should have a parameter to decide weither or not it injects the admin argument into the function call.
def require_admin_for_event(func):
    """
    Ensures that the current user is an administrator account for the given event
    and injects the corresponding Administrator as kwarg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        event_id = kwargs['event_id']
        kwargs['current_admin'] = validate_and_get_current_admin_for_event(event_id)
        return func(*args, **kwargs)
    wrapper.func = func  # To bypass decorator in unit testing
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
    wrapper.func = func  # To bypass decorator in unit testing
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
    wrapper.func = func  # To bypass decorator in unit testing
    return wrapper


def validate_and_get_current_event(event_id: int):
    """
    Check if event with id event_id exists and that the event is visible. If not, return a 404 error.
    """
    event = Event.query.filter_by(id=event_id).first()
    if event is None or not event.is_visible:
        raise errors.NotFound(f"Event with ID {event_id} not found.")
    return event


def require_event(func):
    """
    Decorator that fetches the current event by parsing the URL. Requires an 'event_id' int
    in the request, or a 400 Bad Request is returned. The event must also be visible.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'event_id' not in kwargs:
            raise errors.BadRequest('The request requires an event ID')
        event = validate_and_get_current_event(kwargs['event_id'])

        kwargs['event'] = event
        del kwargs['event_id']
        return func(*args, **kwargs)
    wrapper.func = func  # To bypass decorator in unit testing
    return wrapper


def check_open_event(event: Event):
    """Return a 403 error if the given event in not open."""
    if not event.is_open:
        raise errors.Forbidden('The event is not open.')


def require_open_event(func):
    """
    Decorator that fetches the current event by parsing the URL. Requires an 'event_id' int
    in the request, or a 400 Bad Request is returned. The event must also be visible. It must also
    be opened
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'event_id' not in kwargs:
            raise errors.BadRequest('The request requires an event ID')
        event = validate_and_get_current_event(kwargs['event_id'])

        check_open_event(event)

        kwargs['event'] = event
        del kwargs['event_id']
        return func(*args, **kwargs)
    wrapper.func = func  # To bypass decorator in unit testing
    return wrapper


def require_open_event_for_challenge(func):
    """
    Decorator that fetches the current event by going through the given challenge_id. Requires a 'challenge_id' int
    in the request, or a 400 Bad Request is returned. The event must also be visible. It must also
    be open. Injects the 'challenge' kwarg onto the function and deletes the challenge_id arg.
    Also injects the 'event' kwarg.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'challenge_id' not in kwargs:
            raise errors.BadRequest('The request requires a challenge ID')
        challenge = Challenge.query.filter_by(id=kwargs['challenge_id']).first()

        if challenge is None:
            raise errors.NotFound(f'The challenge with id {kwargs["challenge_id"]} was not found')

        event = Event.query.filter_by(id=challenge.category.event_id).first()
        if event is None or not event.is_visible:
            raise errors.NotFound(f"Event with ID {event.id} not found.")

        check_open_event(event)

        kwargs['challenge'] = challenge
        kwargs['event'] = event
        del kwargs['challenge_id']
        return func(*args, **kwargs)
    wrapper.func = func  # To bypass decorator in unit testing
    return wrapper
