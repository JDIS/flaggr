"""Team routes"""

import flask_rebar
from flask_login import current_user
from flask_rebar import errors

from JDISCTF.app import DB, REGISTRY
from JDISCTF.flask_login_authenticator import FlaskLoginAuthenticator
from JDISCTF.models import Team, TeamMember, TeamRequest
from JDISCTF.schemas import CreateTeamSchema, TeamSchema
from JDISCTF.schemas.team import AcceptTeamRequestRequestSchema, AcceptTeamRequestSchema, \
    ChangeRoleRequestSchema, ChangeRoleSchema, DeclineTeamRequestRequestSchema, \
    DeclineTeamRequestSchema, DeleteTeamRequestRequestSchema, DeleteTeamRequestSchema, \
    KickTeamMemberRequestSchema, KickTeamMemberSchema, SendTeamRequestRequestSchema, \
    SendTeamRequestSchema


@REGISTRY.handles(
    rule="/team",
    method="GET",
    response_body_schema={200: TeamSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def current_team():
    """Current user's team information"""

    team = Team.query.join(TeamMember).filter_by(user_id=current_user.id).first()
    return team


@REGISTRY.handles(
    rule="/teams",
    method="GET",
    response_body_schema={200: TeamSchema(many=True)},
    authenticators=FlaskLoginAuthenticator()
)
def teams_list():
    """ Get teams list for the current event """
    return Team.query.filter_by(event_id=0).join(TeamMember).all()


@REGISTRY.handles(
    rule="/team",
    method="POST",
    request_body_schema=CreateTeamSchema(),
    response_body_schema={200: TeamSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def create_team():
    """Create a team for a given event."""
    body = flask_rebar.get_validated_body()
    name = body["name"]

    team = Team.query.join(TeamMember).filter_by(user_id=current_user.id).first()

    if team is not None:
        raise errors.UnprocessableEntity("You cannot create a team if you already are in a team")

    team = Team.query.filter_by(name=name).first()

    if team is not None:
        raise errors.UnprocessableEntity("A team with that name already exists")

    team = Team(name=name, event_id=current_user.event_id, members=[TeamMember(user_id=current_user.id, captain=True)])

    DB.session.add(team)
    DB.session.commit()
    return team


@REGISTRY.handles(
    rule="/team_request",
    method="POST",
    request_body_schema=SendTeamRequestRequestSchema(),
    response_body_schema={200: SendTeamRequestSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def send_team_request():
    """Request to join a team."""
    body = flask_rebar.get_validated_body()
    team_id = body["team_id"]

    # If user has no team
    teamMember = TeamMember.filter_by(user_id=current_user.id).first()

    if teamMember is not None:
        raise errors.UnprocessableEntity("You cannot request to join a team if you already are in a team")

    # If team exists
    team = Team.query.filter_by(id=team_id).first()

    if team is None:
        raise errors.UnprocessableEntity("The team doesn't exist")

    # FIXME : If team is not already full (on a pas de configuration pour le nombre de membres d'une équipe for now)

    # If user has not already applied (for any team)
    teamRequest = TeamRequest.filter_by(user_id=current_user.id).first()

    if teamRequest is not None:
        raise errors.UnprocessableEntity("You already have requested to join a team")

    teamRequest = TeamRequest(team_id=team_id, user_id=current_user.id)

    DB.session.add(teamRequest)
    DB.session.commit()
    return "team requested"


@REGISTRY.handles(
    rule="/accept_team_request",
    method="POST",
    request_body_schema=AcceptTeamRequestRequestSchema(),
    response_body_schema={200: AcceptTeamRequestSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def accept_team_request():
    """Accepts a team request. Only captains can accept a request."""
    body = flask_rebar.get_validated_body()
    user_id = body["user_id"]

    currentMember = TeamMember.filter_by(user_id=current_user.user_id).first()
    
    if not currentMember and not currentMember.captain:
        raise errors.UnprocessableEntity("You don't have the rights to accept this request.")

    # Remove TeamRequest and add the new member
    teamRequest = TeamRequest.filter_by(user_id=user_id).first()
    newMember = TeamMember(user_id=user_id, team_id=currentMember.team_id)

    DB.session.delete(teamRequest)
    DB.session.add(newMember)
    DB.session.commit()
    # If user has no team
    return None


@REGISTRY.handles(
    rule="/decline_team_request",
    method="POST",
    request_body_schema=DeclineTeamRequestRequestSchema(),
    response_body_schema={200: DeclineTeamRequestSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def decline_team_request():
    """Decline a team request. Only captains can decline a request."""
    body = flask_rebar.get_validated_body()
    user_id = body["user_id"]
    currentMember = TeamMember.filter_by(user_id=current_user.user_id).first()
    
    if not currentMember and not currentMember.captain:
        raise errors.UnprocessableEntity("You don't have the rights to accept this request.")

    # Remove TeamRequest
    teamRequest = TeamRequest.filter_by(user_id=user_id).first()

    DB.session.delete(teamRequest)
    DB.session.commit()
    return None


@REGISTRY.handles(
    rule="/kick_team_member",
    method="POST",
    request_body_schema=KickTeamMemberRequestSchema(),
    response_body_schema={200: KickTeamMemberSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def kick_team_member():
    """Kick a member of the team. Only captains can kick a team member"""
    body = flask_rebar.get_validated_body()
    user_id = body["user_id"]
    currentMember = TeamMember.filter_by(user_id=current_user.user_id).first()

    if not currentMember and not currentMember.captain:
        raise errors.UnprocessableEntity("You don't have the rights to accept this request.")

    if user_id == current_user.user_id:
        raise errors.UnprocessableEntity("You cannot kick yourself from a team.")

    teamMember = TeamMember.filter_by(user_id=user_id).first()

    DB.session.delete(teamMember)
    DB.session.commit()
    return None


@REGISTRY.handles(
    rule="/change_role",
    method="POST",
    request_body_schema=ChangeRoleRequestSchema(),
    response_body_schema={200: ChangeRoleSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def change_role():
    """Change the role of a team member. Only captains can change a team member's role"""
    return None


@REGISTRY.handles(
    rule="/team_request",
    method="DELETE",
    request_body_schema=DeleteTeamRequestRequestSchema(),
    response_body_schema={200: DeleteTeamRequestSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def remove_own_team_request():
    """Remove own request."""

    teamRequest = TeamRequest.filter_by(user_id=current_user.id).first()

    if teamRequest is None:
        raise errors.UnprocessableEntity("A team with that name already exists")

    DB.session.delete(teamRequest)
    DB.session.commit()
    return None


@REGISTRY.handles(
    rule="/leave_team",
    method="POST",
    request_body_schema=DeleteTeamRequestRequestSchema(),
    response_body_schema={200: DeleteTeamRequestSchema()},
    authenticators=FlaskLoginAuthenticator()
)
def leave_team():
    """Leave a team"""

    teamMember = TeamMember.filter_by(user_id=current_user.id).first()

    if teamMember is None:
        raise errors.UnprocessableEntity("You are not in a team.")

    DB.session.delete(teamMember)
    DB.session.commit()
    return None
