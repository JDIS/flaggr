"""Challenges routes"""

import flask_rebar
from flask_rebar import errors
from JDISCTF.app import REGISTRY
from JDISCTF.schemas import ChallengeSchema
from JDISCTF.models import Challenge, Category, Event


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
    response_body_schema=ChallengeSchema
)
def get_challenge(challenge_id: int):
    """Get a single challenge by its id"""
    challenge = Challenge.query.filter_by(id=challenge_id).first()

    if challenge is None:
        raise errors.NotFound()

    return challenge
