"""Categories routes"""
import flask_rebar
from flask_rebar import errors

from JDISCTF.app import DB, REGISTRY
from JDISCTF.flask_login_authenticator import FlaskLoginAuthenticator
from JDISCTF.models import Category, Event
from JDISCTF.schemas.admin import AdminCategorySchema, AdminCategoryRequestSchema


@REGISTRY.handles(
    rule="/admin/categories/event/<int:event_id>",
    method="GET",
    response_body_schema=AdminCategorySchema(many=True)
    # Commented for dev
    # TOOD : Admin-only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def get_admin_categories(event_id: int):
    """Get all the categories for a given event"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    categories = Category.query.filter_by(event_id=event_id).all()

    return categories

@REGISTRY.handles(
    rule="/admin/categories",
    method="POST",
    request_body_schema=AdminCategoryRequestSchema(),
    response_body_schema=AdminCategorySchema(),
    # Commented for dev
    # TOOD : Admin-only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def create_category():
    """Add a category """
    body = flask_rebar.get_validated_body()
    name = body["name"]
    event_id = body["event_id"]

    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    category = Category.query.filter_by(name=name, event_id=event_id).first()

    if category is not None:
        raise errors.UnprocessableEntity("A category with that name already exists")

    category = Category(name=name, event_id=event_id)

    DB.session.add(category)
    DB.session.commit()

    return category
