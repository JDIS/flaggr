"""Challenges routes"""

from flask_rebar import errors
from JDISCTF.app import REGISTRY
from JDISCTF.schemas import ChallengeSchema, ChallengeByCategorySchema
from JDISCTF.models import Challenge, Category, Event
from sqlalchemy.orm import contains_eager


@REGISTRY.handles(
    rule="/challenges/event/<int:event_id>",
    method="GET",
    response_body_schema=ChallengeSchema(many=True)
)
def get_all_challenges_for_event(event_id: int):
    # pylint: disable=singleton-comparison
    """Get all the challenges for a given event"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    challenges = Challenge.query.join(Category).join(Event) \
        .filter(Event.id == event_id, Challenge.hidden == False).all()

    return challenges


@REGISTRY.handles(
    rule="/challenges/<int:challenge_id>",
    method="GET",
    response_body_schema=ChallengeSchema()
)
def get_challenge(challenge_id: int):
    """Get a single challenge by its id"""
    challenge = Challenge.query.filter_by(id=challenge_id, hidden=False).first()

    if challenge is None:
        raise errors.NotFound(f'Challenge with id "{challenge_id}" not found.')

    return challenge


@REGISTRY.handles(
    rule="/challenges/event/<int:event_id>/by-category",
    method="GET",
    response_body_schema=ChallengeByCategorySchema(many=True)
)
def get_all_challenges_by_category_for_event(event_id: int):
    # pylint: disable=singleton-comparison
    """Get all the challenges for an event, grouped by category"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    categories = Category.query \
        .join(Category.challenges)\
        .options(contains_eager(Category.challenges))\
        .filter(Category.event_id == event_id, Challenge.hidden == False)\
        .all()
    return categories
