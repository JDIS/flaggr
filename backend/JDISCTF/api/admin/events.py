"""Categories routes"""
import flask_rebar
from flask_rebar import errors

from JDISCTF.app import DB, REGISTRY
from JDISCTF.flask_login_authenticator import FlaskLoginAuthenticator
from JDISCTF.models import Event

from JDISCTF.schemas import GenericMessageSchema
from JDISCTF.schemas.admin import AdminEventListSchema, AdminEventSchema, AdminEventRequestSchema


@REGISTRY.handles(
    rule="/admin/events",
    method="GET",
    response_body_schema=AdminEventListSchema(many=True)
    # Commented for dev
    # TOOD : Platform-admin only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def get_admin_events():
    """Get all the events"""
    events = Event.query.filter_by().all()

    return events


@REGISTRY.handles(
    rule="/admin/event/<int:event_id>",
    method="DELETE",
    response_body_schema=GenericMessageSchema()
    # Commented for dev
    # TOOD : Platform-admin only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def delete_event(event_id: int):
    """Delete an event"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    DB.session.delete(event)
    DB.session.commit()

    return ""


@REGISTRY.handles(
    rule="/admin/events",
    method="POST",
    request_body_schema=AdminEventRequestSchema(),
    response_body_schema=AdminEventSchema()
    # Commented for dev
    # Platform-admin only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def create_event():
    """Create a new event"""
    body = flask_rebar.get_validated_body()
    name = body["name"]
    teams = body["teams"]
    is_open = body["is_open"]
    is_visible = body["is_visible"]
    url = body["url"] if "url" in body else ""
    front_page = body["front_page"] if "front_page" in body else ""
    flag_format = body["flag_format"] if "flag_format" in body else ""

    event = Event.query.filter_by(name=name).first()

    if event:
        raise errors.UnprocessableEntity("An event with that name already exists")

    event = Event(name=name, url=url, front_page=front_page, flag_format=flag_format,
                  is_open=is_open, is_visible=is_visible, teams=teams)

    DB.session.add(event)
    DB.session.commit()

    return event


@REGISTRY.handles(
    rule="/admin/event/<int:event_id>",
    method="PUT",
    request_body_schema=AdminEventRequestSchema(),
    response_body_schema=AdminEventSchema()
    # Commented for dev
    # Platform-admin only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def edit_event(event_id: int):
    """Create a new event"""
    body = flask_rebar.get_validated_body()
    name = body["name"]
    teams = body["teams"]
    is_open = body["is_open"]
    is_visible = body["is_visible"]
    url = body["url"] if "url" in body else ""
    front_page = body["front_page"] if "front_page" in body else ""
    flag_format = body["flag_format"] if "flag_format" in body else ""

    editable_event = Event.query.filter_by(id=event_id).first()

    if editable_event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    if name != editable_event.name:
        if not name:
            raise errors.UnprocessableEntity("Name must not be empty.")

        event = Event.query.filter_by(name=name).first()

        if event is not None:
            raise errors.UnprocessableEntity("An event with that name already exists.")

    event = Event(name=name, url=url, front_page=front_page, flag_format=flag_format,
                  is_open=is_open, is_visible=is_visible, teams=teams)

    DB.session.add(event)
    DB.session.commit()

    return event
