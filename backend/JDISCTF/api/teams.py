"""Team routes"""

import flask_rebar
from flask_rebar import errors
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Team, TeamMember, User
from JDISCTF.schemas import CreateTeamSchema, CreateUserSchema, LoginSchema, LogoutSchema, TeamSchema, UserSchema



@REGISTRY.handles(
    rule="/team",
    method="GET",
    response_body_schema={200: TeamSchema()},
)
@login_required
def current_team():
    """Current user's team information"""
    """TODO :)"""
    team = TeamMember.query.filter_by(user_id=current_user.id).first().team
    return team


@REGISTRY.handles(
    rule="/team",
    method="POST",
    request_body_schema=CreateTeamSchema(),
    response_body_schema={200: TeamSchema()},
)
@login_required
def create_team():
    """Create a team for a given event."""
    body = flask_rebar.get_validated_body()
    name = body["name"]

    # TODO : If current user has no team (team relationship on user?)
    team = Team.query.filter_by(name=name).first()

    if team is not None:
        raise errors.UnprocessableEntity("A team with that name already exists")

    team = Team(name=name, event_id=current_user.event_id, members=[TeamMember(user_id=current_user.id, captain=True)])

    DB.session.add(team)
    DB.session.commit()
    return team


def accept_team_request():
    """TODO :)"""
    return None


def leave_team():
    """TODO :)"""
    return None


def kick_team_member():
    """TODO :)"""
    return None

def change_role():
    """TODO :)"""
    return None