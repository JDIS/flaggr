"""Event routes"""

from JDISCTF.app import REGISTRY
from JDISCTF.models import Event
from JDISCTF.permission_wrappers import require_event
from JDISCTF.schemas.event import EventSchema


@REGISTRY.handles(
    rule="/event/<int:event_id>",
    method="GET",
    response_body_schema={200: EventSchema()},
    authenticators=None
)
@require_event
def get_event(event: Event):
    """Get an event"""

    return event


@REGISTRY.handles(
    rule="/event/all",
    method="GET",
    response_body_schema={200: EventSchema(many=True)},
    authenticators=None
)
def get_all_events():
    """Get the list of all events"""

    return Event.query.filter_by(is_visible=True).all()
