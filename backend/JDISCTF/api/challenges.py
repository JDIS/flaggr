"""Challenges routes"""
import re
import flask_rebar
from flask_rebar import errors
from JDISCTF.app import REGISTRY, DB
from JDISCTF.schemas import ChallengeSchema, ChallengeByCategorySchema, SubmitFlagSchema, \
    SubmitFlagResponseSchema
from JDISCTF.models import Challenge, Category, Event, Team, Flag, Submission
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
        .join(Category.challenges) \
        .options(contains_eager(Category.challenges)) \
        .filter(Category.event_id == event_id, Challenge.hidden == False) \
        .all()
    return categories


@REGISTRY.handles(
    rule="/challenges/<int:challenge_id>/submit",
    method="POST",
    request_body_schema=SubmitFlagSchema(),
    response_body_schema=SubmitFlagResponseSchema()
)
def submit_flag(challenge_id: int):
    """Submit a flag for a given challenge"""
    challenge = Challenge.query.filter_by(hidden=False, id=challenge_id).first()

    if challenge is None:
        raise errors.NotFound(f'Challenge with id "{challenge_id}" not found.')

    body = flask_rebar.get_validated_body()
    team_id = body["team_id"]
    submitted_flag = body["flag"]

    team = Team.query.get(team_id)

    if team is None:
        raise errors.NotFound(f'Team with id "{team_id}" not found.')

    challenge_event_id = DB.session.query(Category.event_id) \
        .join(Category.challenges) \
        .filter(Challenge.id == challenge_id) \
        .first()[0]

    if challenge_event_id != team.event_id:
        raise errors.UnprocessableEntity(
            f'Team "{team_id}" and challenge "{challenge_id}" are not part of the same event')

    submission = Submission(team_id=team_id, challenge_id=challenge_id, input=submitted_flag)

    flags = Flag.query.filter_by(challenge_id=challenge_id).all()

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
