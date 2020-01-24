"""Participants routes"""

from JDISCTF.app import REGISTRY
from JDISCTF.models import Administrator, Participant
from JDISCTF.permission_wrappers import require_admin_for_event
from JDISCTF.schemas.admin.participants import AdminParticipantListSchema


@REGISTRY.handles(
    rule="/admin/event/<int:event_id>/participants",
    method="GET",
    response_body_schema=AdminParticipantListSchema(many=True)
)
@require_admin_for_event
def get_participants_for_events(event_id: int, current_admin: Administrator):
    """Get all the events"""
    # pylint: disable=unused-argument
    participants = Participant.query.filter_by(event_id=event_id).join(Participant.user).all()

    return participants
