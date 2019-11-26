"""Team routes"""

import flask_rebar
from flask_rebar import errors
from sqlalchemy.orm import contains_eager

from JDISCTF.app import DB, REGISTRY
from JDISCTF.flask_login_authenticator import FlaskLoginAuthenticator
from JDISCTF.models import Participant, Team, TeamMember, TeamRequest
from JDISCTF.permission_wrappers import require_participant
from JDISCTF.schemas import AcceptTeamRequestRequestSchema, \
    ChangeRoleRequestSchema, CreateTeamRequestSchema, DeclineTeamRequestRequestSchema, \
    GenericMessageSchema, KickTeamMemberRequestSchema, SendTeamRequestRequestSchema, \
    TeamRequestSchema, TeamSchema


@REGISTRY.handles(
    rule="/team",
    method="GET",
    response_body_schema={200: TeamSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def current_team(current_participant: Participant):
    """Current user's team information"""

    return current_participant.get_team()


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
    request_body_schema=CreateTeamRequestSchema(),
    response_body_schema={200: TeamSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def create_team(current_participant: Participant):
    """Create a team for a given event."""
    body = flask_rebar.get_validated_body()
    team_name = body["team_name"]

    team = current_participant.get_team()

    if team is not None:
        raise errors.UnprocessableEntity("You cannot create a team if you already are in a team.")

    team = Team.query.filter_by(name=team_name).first()

    if team is not None:
        raise errors.UnprocessableEntity("A team with that name already exists.")

    team = Team(name=team_name, event_id=current_participant.event_id,
                members=[TeamMember(participant_id=current_participant.id, captain=True)])

    DB.session.add(team)
    DB.session.commit()
    return team


@REGISTRY.handles(
    rule="/team_request",
    method="GET",
    response_body_schema={200: TeamRequestSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def get_team_request(current_participant: Participant):
    """Get the request for the current user (if any)."""
    team_request = TeamRequest.query \
        .filter_by(participant_id=current_participant.id) \
        .join(TeamRequest.team) \
        .options(contains_eager(TeamRequest.team)) \
        .join(Team.members) \
        .first()

    return team_request


@REGISTRY.handles(
    rule="/team_request",
    method="POST",
    request_body_schema=SendTeamRequestRequestSchema(),
    response_body_schema={200: GenericMessageSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def send_team_request(current_participant: Participant):
    """Request to join a team."""
    body = flask_rebar.get_validated_body()
    team_id = body["team_id"]

    team_member = current_participant.get_team()

    if team_member is not None:
        raise errors.UnprocessableEntity("You cannot request to join a team if you already are in a team.")

    team = Team.query.filter_by(id=team_id).first()

    if team is None:
        raise errors.UnprocessableEntity("The team doesn't exist.")

    # FIXMEFUTURE: If team is not already full
    # (on a pas de configuration pour le nombre de membres d'une équipe for now)
    team_request = TeamRequest.query.filter_by(participant_id=current_participant.id).first()

    if team_request is not None:
        raise errors.UnprocessableEntity("You already have requested to join a team.")

    team_request = TeamRequest(team_id=team_id, participant_id=current_participant.id)

    DB.session.add(team_request)
    DB.session.commit()
    return ""


@REGISTRY.handles(
    rule="/accept_team_request",
    method="POST",
    request_body_schema=AcceptTeamRequestRequestSchema(),
    response_body_schema={200: GenericMessageSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def accept_team_request(current_participant: Participant):
    """Accepts a team request. Only captains can accept a request."""
    body = flask_rebar.get_validated_body()
    participant_id = body["participant_id"]

    current_member = TeamMember.query.filter_by(participant_id=current_participant.id).first()

    if not current_member or not current_member.captain:
        raise errors.Unauthorized("You don't have the rights to accept this request.")

    # Remove TeamRequest and add the new member
    team_request = TeamRequest.query.filter_by(team_id=current_member.team_id, participant_id=participant_id).first()

    if team_request is None:
        raise errors.UnprocessableEntity("The request doesn't exist.")

    new_member = TeamMember(participant_id=participant_id, team_id=current_member.team_id)

    DB.session.delete(team_request)
    DB.session.add(new_member)
    DB.session.commit()

    return ""


@REGISTRY.handles(
    rule="/decline_team_request",
    method="POST",
    request_body_schema=DeclineTeamRequestRequestSchema(),
    response_body_schema={200: GenericMessageSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def decline_team_request(current_participant: Participant):
    """Decline a team request. Only captains can decline a request."""
    body = flask_rebar.get_validated_body()
    participant_id = body["participant_id"]
    current_member = TeamMember.query.filter_by(participant_id=current_participant.id).first()

    if not current_member or not current_member.captain:
        raise errors.Unauthorized("You don't have the rights to decline this request.")

    # Remove TeamRequest
    team_request = TeamRequest.query.filter_by(team_id=current_member.team_id, participant_id=participant_id).first()

    if team_request is None:
        raise errors.UnprocessableEntity("The request doesn't exist.")

    DB.session.delete(team_request)
    DB.session.commit()
    return ""


@REGISTRY.handles(
    rule="/kick_team_member",
    method="POST",
    request_body_schema=KickTeamMemberRequestSchema(),
    response_body_schema={200: GenericMessageSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def kick_team_member(current_participant: Participant):
    """Kick a member of the team. Only captains can kick a team member"""
    body = flask_rebar.get_validated_body()
    participant_id = body["participant_id"]
    current_member = TeamMember.query.filter_by(participant_id=current_participant.id).first()

    if not current_member or not current_member.captain:
        raise errors.Unauthorized("You don't have the rights to kick a team member.")

    if participant_id == current_participant.id:
        raise errors.UnprocessableEntity("You cannot kick yourself from a team.")

    team_member = TeamMember.query.filter_by(participant_id=participant_id).first()

    DB.session.delete(team_member)
    DB.session.commit()
    return ""


@REGISTRY.handles(
    rule="/change_role",
    method="POST",
    request_body_schema=ChangeRoleRequestSchema(),
    response_body_schema={200: GenericMessageSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def change_role(current_participant: Participant):
    """Change the role of a team member. Only captains can change a team member's role"""
    body = flask_rebar.get_validated_body()
    participant_id = body["participant_id"]
    new_role = body["captain"]

    current_member = TeamMember.query.filter_by(participant_id=current_participant.id).first()

    if not current_member or not current_member.captain:
        raise errors.Unauthorized("You don't have the rights to change a team member's role.")

    if participant_id == current_participant.id:
        # In order to avoid a team "bricking" itself
        raise errors.UnprocessableEntity("You cannot remove your own privileges.")

    team_member = TeamMember.query.filter_by(participant_id=participant_id).first()
    team_member.captain = new_role

    DB.session.commit()
    return ""


@REGISTRY.handles(
    rule="/team_request",
    method="DELETE",
    response_body_schema={200: GenericMessageSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def remove_own_team_request(current_participant: Participant):
    """Remove own request."""

    team_request = TeamRequest.query.filter_by(participant_id=current_participant.id).first()

    if team_request is None:
        raise errors.UnprocessableEntity("You don't have any pending requests.")

    DB.session.delete(team_request)
    DB.session.commit()
    return ""


@REGISTRY.handles(
    rule="/leave_team",
    method="POST",
    response_body_schema={200: GenericMessageSchema()},
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def leave_team(current_participant: Participant):
    """Leave a team"""
    # NOTE: When the last member of a team leaves, what should happen? We do not want to delete a team.

    team_member = TeamMember.query.filter_by(participant_id=current_participant.id).first()

    if team_member is None:
        raise errors.UnprocessableEntity("You are not in a team.")

    DB.session.delete(team_member)
    DB.session.commit()
    return ""
