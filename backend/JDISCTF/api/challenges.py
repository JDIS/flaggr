"""Challenges routes"""

from flask_rebar import errors
from JDISCTF.app import REGISTRY
from JDISCTF.schemas import ChallengeSchema, ChallengeByCategorySchema
from JDISCTF.models import Challenge, Category, Event
from sqlalchemy.orm import joinedload


@REGISTRY.handles(
    rule="/challenges/event/<int:event_id>",
    method="GET",
    response_body_schema=ChallengeSchema(many=True)
)
def get_all_challenges_for_event(event_id: int):
    """Get all the challenges for a given event"""
    challenges = Challenge.query.join(Category).join(Event).filter(Event.id == event_id).all()

    return challenges


@REGISTRY.handles(
    rule="/challenges/<int:challenge_id>",
    method="GET",
    response_body_schema=ChallengeSchema()
)
def get_challenge(challenge_id: int):
    """Get a single challenge by its id"""
    challenge = Challenge.query.filter_by(id=challenge_id).first()

    if challenge is None:
        raise errors.NotFound(f'Challenge with id "{challenge_id}" not found.')

    return challenge


@REGISTRY.handles(
    rule="/challenges/event/<int:event_id>/by-category",
    method="GET",
    response_body_schema=ChallengeByCategorySchema(many=True)
)
def get_challenges_by_category(event_id: int):
    """Get all the challenges for an event, grouped by category"""
    categories = Category.query\
        .options(joinedload(Category.challenges, innerjoin=True))\
        .filter_by(event_id=event_id)\
        .all()
    return categories
