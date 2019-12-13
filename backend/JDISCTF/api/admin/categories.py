"""Categories routes"""
import flask_rebar
from flask_rebar import errors

from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Administrator, Category, Event
from JDISCTF.permission_wrappers import require_admin, require_admin_for_event
from JDISCTF.schemas.admin import AdminCategorySchema, AdminCategoryRequestSchema


@REGISTRY.handles(
    rule="/admin/categories/event/<int:event_id>",
    method="GET",
    response_body_schema=AdminCategorySchema(many=True)
)
@require_admin_for_event
def get_admin_categories(_: Administrator, event_id: int):
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
    response_body_schema=AdminCategorySchema()
)
@require_admin
def create_category(current_admin: Administrator):
    """Add a category """
    body = flask_rebar.get_validated_body()
    name = body["name"]
    event_id = body["event_id"]

    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    if not current_admin.is_admin_of_event(event_id):
        raise errors.Unauthorized("You do not have the permission to administer this category.")

    category = Category.query.filter_by(name=name, event_id=event_id).first()

    if category is not None:
        raise errors.UnprocessableEntity("A category with that name already exists")

    category = Category(name=name, event_id=event_id)

    DB.session.add(category)
    DB.session.commit()

    return category
