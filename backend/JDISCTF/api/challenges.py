"""Challenges routes"""
import re

import flask_rebar
from flask_login import current_user
from flask_rebar import errors
from sqlalchemy.orm import contains_eager

from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Category, Challenge, Event, Flag, Submission
from JDISCTF.permission_wrappers import require_open_event, \
    require_open_event_for_challenge
from JDISCTF.schemas import ChallengeByCategorySchema, SubmitFlagResponseSchema, SubmitFlagSchema, \
    UserChallengeSchema


@REGISTRY.handles(
    rule="/event/<int:event_id>/challenges",
    method="GET",
    response_body_schema=UserChallengeSchema(many=True)
)
@require_open_event
def get_all_challenges_for_event(event: Event):
    # pylint: disable=singleton-comparison
    """Get all the challenges for a given event"""

    completed_stmt = Submission.query \
        .filter(Submission.challenge_id == Challenge.id, Submission.is_correct == True) \
        .exists() \
        .label('completed')

    challenges = DB.session.query(Challenge, completed_stmt).join(Category).join(Event) \
        .filter(Event.id == event.id, Challenge.hidden == False).all()

    for challenge in challenges:
        challenge.Challenge.completed = challenge[1]

    return map(lambda x: x.Challenge, challenges)


@REGISTRY.handles(
    rule="/event/<int:event_id>/challenges/by-category",
    method="GET",
    response_body_schema=ChallengeByCategorySchema(many=True)
)
@require_open_event
def get_all_challenges_by_category_for_event(event: Event):
    # pylint: disable=singleton-comparison
    """Get all the challenges for an event, grouped by category"""

    categories = Category.query \
        .join(Category.challenges) \
        .options(contains_eager(Category.challenges)) \
        .filter(Category.event_id == event.id, Challenge.hidden == False) \
        .all()
    for category in categories:
        for challenge in category.challenges:
            challenge.is_solved = any(solve.team_id == current_user.get_team().id for solve in challenge.solves)
    return categories


@REGISTRY.handles(
    rule="/challenges/<int:challenge_id>/submit",
    method="POST",
    request_body_schema=SubmitFlagSchema(),
    response_body_schema=SubmitFlagResponseSchema()
)
@require_open_event_for_challenge
def submit_flag(challenge: Challenge, event: Event):
    """Submit a flag for a given challenge"""

    body = flask_rebar.get_validated_body()
    submitted_flag = body["flag"]

    team = current_user.get_team()

    if team is None:
        raise errors.NotFound(f'Current user has no team.')

    if event.id != team.event_id:
        raise errors.UnprocessableEntity(
            f'Team "{team.name}" and challenge "{challenge.id}" are not part of the same event')

    submission = Submission(team_id=team.id, challenge_id=challenge.id, input=submitted_flag)

    flags = Flag.query.filter_by(challenge_id=challenge.id).all()

    is_correct = any(validate_flag(x, submitted_flag) for x in flags)
    submission.is_correct = is_correct

    DB.session.add(submission)
    DB.session.commit()

    return {'correct': is_correct}


def validate_flag(flag: Flag, submitted_value: str) -> bool:
    """Checks whether a flag is a valid solution or not"""
    if flag.is_regex:
        pattern = re.compile(flag.value)
        return pattern.match(submitted_value) is not None

    return flag.value == submitted_value
