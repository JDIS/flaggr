"""Event routes"""

from JDISCTF.app import REGISTRY
from JDISCTF.models import Event
from JDISCTF.permission_wrappers import require_event
from JDISCTF.schemas.event import EventSchema


@REGISTRY.handles(
    rule="/event/<int:event_id>",
    method="GET",
    response_body_schema={200: EventSchema()},
)
@require_event
def get_event(event: Event):
    """Get an event"""

    return event
