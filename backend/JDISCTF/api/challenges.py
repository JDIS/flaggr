from JDISCTF.app import REGISTRY
from JDISCTF.schemas import ChallengeSchema
from JDISCTF.models import Challenge, Category, Event


@REGISTRY.handles(
    rule="/challenges/<int:event_id>",
    method="GET",
    response_body_schema=ChallengeSchema(many=True)
)
def get_all_challenges_for_event(event_id: int):
    challenges = Challenge.query.join(Category).join(Event).filter(Event.id == event_id).all()

    return challenges
