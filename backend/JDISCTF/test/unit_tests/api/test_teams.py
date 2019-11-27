import importlib
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api import teams, teams_list
from JDISCTF.models import Event, Participant, Team, TeamMember, TeamRequest, User


def local_patch(module: str, **kwargs):
    return patch('JDISCTF.api.teams.' + module, **kwargs)


@fixture
def team_mock():
    with local_patch('Team') as mock:
        yield mock


@fixture
def team_member_mock():
    with local_patch('TeamMember') as mock:
        yield mock


@fixture
def team_request_mock():
    with local_patch('TeamRequest') as mock:
        yield mock


@fixture
def rebar_mock():
    with local_patch('flask_rebar') as mock:
        yield mock


@fixture
def db_mock():
    with local_patch('DB') as mock:
        yield mock


@fixture(autouse=True)
def current_participant_mock():
    with patch('JDISCTF.permission_wrappers.require_participant', lambda x: x):
        with local_patch('Participant') as mock:
            importlib.reload(sys.modules['JDISCTF.api.teams'])
            yield mock

    importlib.reload(sys.modules['JDISCTF.api.teams'])


A_EVENT = Event(id=0, name="Test Event", teams=True)

A_USER = User(id=0, username="test", email="test@gmail.com")
A_USER.set_password("test")

A_PARTICIPANT = Participant(id=0, user_id=A_USER.id, event_id=A_EVENT.id)

A_USER_WITHOUT_TEAM = User(id=1, username="test2", email="test2@gmail.com")
A_USER_WITHOUT_TEAM.set_password("test2")

A_PARTICIPANT_WITHOUT_TEAM = Participant(id=1, user_id=A_USER_WITHOUT_TEAM.id, event_id=A_EVENT.id)

A_USER_NOT_CAPTAIN = User(id=2, username="test3", email="test3@gmail.com")
A_USER_NOT_CAPTAIN.set_password("test3")

A_PARTICIPANT_NOT_CAPTAIN = Participant(id=2, user_id=A_USER_NOT_CAPTAIN.id, event_id=A_EVENT.id)

A_TEAM = Team(id=0, name="Test Team", event_id=A_EVENT.id,
              members=[TeamMember(participant_id=A_PARTICIPANT.id, captain=True),
                       TeamMember(participant_id=A_PARTICIPANT_NOT_CAPTAIN.id, captain=False)])


class TestCurrentTeam:
    def test_given_a_user_without_a_team(self, current_participant_mock: MagicMock):
        current_participant_mock.get_team.return_value = None
        result = teams.current_team(current_participant_mock)

        assert result is None

    def test_given_a_user_with_a_team(self, current_participant_mock: MagicMock):
        current_participant_mock.get_team.return_value = A_TEAM
        result = teams.current_team(current_participant_mock)

        assert result == A_TEAM


class TestTeamsList:
    def test_should_return_all_lists_for_event(self, team_mock):
        team_mock.query.filter_by.return_value.join.return_value.all.return_value = [A_TEAM]
        teams = teams_list(event_id=0)
        assert teams == [A_TEAM]


class TestCreateTeam:
    REQUEST_BODY = {"team_name": "Test Team"}

    A_NEW_TEAM = Team(id=None, name=REQUEST_BODY["team_name"], event_id=A_PARTICIPANT.event_id,
                      members=[TeamMember(participant_id=A_PARTICIPANT_WITHOUT_TEAM.id, captain=True)])

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _team_mock(self, team_mock: MagicMock):
        team_mock.side_effect = lambda *args, **kwargs: Team(*args, **kwargs)

    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        yield db_mock

    def test_given_a_user_already_in_a_team_should_raise_unprocessable_entity_error(self,
                                                                                    current_participant_mock: MagicMock):
        current_participant_mock.get_team.return_value = A_TEAM

        with raises(errors.UnprocessableEntity):
            teams.create_team(current_participant_mock)

    def test_given_an_already_existing_team_name_should_raise_unprocessable_entity_error(self,
                                                                                         team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = A_TEAM

        with raises(errors.UnprocessableEntity):
            teams.create_team(A_PARTICIPANT)

    def test_should_create_a_team(self, db_mock: MagicMock, team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = None

        teams.create_team(A_PARTICIPANT)

        db_mock.session.add.assert_called_with(self.A_NEW_TEAM)

        db_mock.session.commit.assert_called_once()

    def test_should_return_created_team(self, team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = None
        team = teams.create_team(A_PARTICIPANT)
        assert team == self.A_NEW_TEAM


class TestGetTeamRequest:
    def test_should_return_current_participant_team_request(self, team_request_mock: MagicMock):
        a_team_request = TeamRequest(id=0, participant_id=1, team_id=2, requested_at=datetime.now())
        result = team_request_mock.query.filter_by.return_value.first.return_value = a_team_request
        assert result == a_team_request


class TestSendTeamRequest:
    A_TEAM_REQUEST = TeamRequest(participant_id=A_PARTICIPANT_WITHOUT_TEAM.id, team_id=A_TEAM.id)
    REQUEST_BODY = {"team_id": A_TEAM_REQUEST.team_id}

    @fixture(autouse=True)
    def _team_mock(self, team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = A_TEAM

        yield team_mock

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _team_request_mock(self, team_request_mock: MagicMock):
        team_request_mock.side_effect = lambda *args, **kwargs: TeamRequest(*args, **kwargs)

    def test_given_a_user_already_in_a_team_should_raise_unprocessable_entity_error(self,
                                                                                    current_participant_mock: MagicMock):
        current_participant_mock.get_team.return_value = A_TEAM

        with raises(errors.UnprocessableEntity):
            teams.send_team_request(A_PARTICIPANT)

    def test_given_an_non_existent_team_id_should_raise_unprocessable_entity_error(self,
                                                                                   team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            teams.send_team_request(A_PARTICIPANT)

    def test_given_a_user_with_team_request_should_raise_unprocessable_entity_error(self, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value \
            = {"user_id": A_USER_WITHOUT_TEAM.id, "team_id": A_TEAM.id}

        with raises(errors.UnprocessableEntity):
            teams.send_team_request(A_PARTICIPANT)

    def test_should_send_team_request(self, db_mock: MagicMock, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value = None

        teams.send_team_request(A_PARTICIPANT)

        db_mock.session.add.assert_called_with(TeamRequest(participant_id=A_PARTICIPANT.id,
                                                           team_id=self.A_TEAM_REQUEST.team_id))
        db_mock.session.commit.assert_called_once()


class TestAcceptTeamRequest:
    A_TEAM_REQUEST = TeamRequest(team_id=A_TEAM.members[0].team_id, participant_id=A_PARTICIPANT_WITHOUT_TEAM.id)
    A_TEAM_MEMBER = TeamMember(team_id=A_TEAM.members[0].team_id, participant_id=A_PARTICIPANT_WITHOUT_TEAM.id)
    REQUEST_BODY = {"participant_id": A_TEAM_REQUEST.participant_id}

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY

        yield rebar_mock

    @fixture(autouse=True)
    def _team_member_mock(self, team_member_mock):
        team_member_mock.side_effect = lambda *args, **kwargs: TeamMember(*args, **kwargs)

    def test_given_a_user_without_team_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.Unauthorized):
            teams.accept_team_request(A_PARTICIPANT)

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = A_TEAM.members[1]

        with raises(errors.Unauthorized):
            teams.accept_team_request(A_PARTICIPANT)

    def test_given_an_invalid_user_id_should_raise_unprocessable_entity_error(self,
                                                                              team_member_mock: MagicMock,
                                                                              team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = A_TEAM.members[0]
        team_request_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            teams.accept_team_request(A_PARTICIPANT)

    def test_should_delete_team_request_and_add_user_to_team(self,
                                                             db_mock: MagicMock,
                                                             team_member_mock: MagicMock,
                                                             team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = A_TEAM.members[0]
        team_request_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_REQUEST

        teams.accept_team_request(A_PARTICIPANT)

        db_mock.session.delete.assert_called_with(
            TeamRequest(participant_id=self.A_TEAM_REQUEST.participant_id, team_id=self.A_TEAM_REQUEST.team_id))
        db_mock.session.add.assert_called_with(
            TeamMember(participant_id=self.A_TEAM_MEMBER.participant_id, team_id=self.A_TEAM_MEMBER.team_id))
        db_mock.session.commit.assert_called_once()


class TestDeclineTeamRequest:
    A_TEAM_REQUEST = TeamRequest(team_id=A_TEAM.members[0].team_id, participant_id=A_PARTICIPANT_WITHOUT_TEAM.id)
    REQUEST_BODY = {"participant_id": A_TEAM_REQUEST.participant_id}

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY

        yield rebar_mock

    def test_given_a_user_without_team_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.Unauthorized):
            teams.decline_team_request(A_PARTICIPANT)

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = \
            TeamMember(participant_id=A_PARTICIPANT_NOT_CAPTAIN.id, captain=False)

        with raises(errors.Unauthorized):
            teams.decline_team_request(A_PARTICIPANT)

    def test_given_an_invalid_user_id_should_raise_unprocessable_entity_error(self,
                                                                              team_member_mock: MagicMock,
                                                                              team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(participant_id=A_PARTICIPANT.id,
                                                                                      captain=True)
        team_request_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            teams.decline_team_request(A_PARTICIPANT)

    def test_should_delete_team_request(self,
                                        db_mock: MagicMock,
                                        team_member_mock: MagicMock,
                                        team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(participant_id=A_PARTICIPANT.id,
                                                                                      captain=True)
        team_request_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_REQUEST

        teams.decline_team_request(A_PARTICIPANT)

        db_mock.session.delete.assert_called_with(TeamRequest(participant_id=self.A_TEAM_REQUEST.participant_id,
                                                              team_id=self.A_TEAM_REQUEST.team_id))
        db_mock.session.commit.assert_called_once()


class TestKickTeamMember:
    A_TEAM_MEMBER = TeamMember(team_id=A_TEAM.id, participant_id=A_PARTICIPANT_NOT_CAPTAIN.id)
    REQUEST_BODY = {"participant_id": A_TEAM_MEMBER.participant_id}

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    def test_given_a_user_without_team_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.Unauthorized):
            teams.kick_team_member(A_PARTICIPANT)

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = \
            TeamMember(participant_id=A_PARTICIPANT_NOT_CAPTAIN.id, captain=False)

        with raises(errors.Unauthorized):
            teams.kick_team_member(A_PARTICIPANT)

    def test_given_the_current_participant_id_should_raise_unprocessable_entity_error(self,
                                                                               team_member_mock: MagicMock,
                                                                               _rebar_mock: MagicMock):
        _rebar_mock.get_validated_body.return_value = {"participant_id": A_PARTICIPANT.id}
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(participant_id=A_PARTICIPANT.id,
                                                                                      captain=True)

        with raises(errors.UnprocessableEntity):
            teams.kick_team_member(A_PARTICIPANT)

    def test_should_delete_team_member(self, db_mock: MagicMock, team_member_mock: MagicMock):
        # Multiple call needs to return different things
        team_member_mock.query.filter_by.return_value.first.side_effect = \
            [TeamMember(participant_id=A_PARTICIPANT.id, captain=True), self.A_TEAM_MEMBER]

        teams.kick_team_member(A_PARTICIPANT)

        db_mock.session.delete.assert_called_with(TeamMember(participant_id=self.A_TEAM_MEMBER.participant_id,
                                                             team_id=self.A_TEAM_MEMBER.team_id))
        db_mock.session.commit.assert_called_once()


class TestChangeRole:
    REQUEST_BODY = {"participant_id": A_PARTICIPANT_NOT_CAPTAIN.id, "captain": True}

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    def test_given_a_user_without_team_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.Unauthorized):
            teams.change_role(A_PARTICIPANT)

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = \
            TeamMember(participant_id=A_PARTICIPANT_NOT_CAPTAIN.id, captain=False)

        with raises(errors.Unauthorized):
            teams.change_role(A_PARTICIPANT)

    def test_given_the_current_participant_id_should_raise_unprocessable_entity_error(self,
                                                                               team_member_mock: MagicMock,
                                                                               _rebar_mock: MagicMock):
        _rebar_mock.get_validated_body.return_value = {"participant_id": A_PARTICIPANT.id, "captain": True}
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(participant_id=A_PARTICIPANT.id,
                                                                                      captain=True)

        with raises(errors.UnprocessableEntity):
            teams.change_role(A_PARTICIPANT)

    def test_should_commit_changes(self, db_mock: MagicMock, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(participant_id=A_PARTICIPANT.id,
                                                                                      captain=True)

        teams.change_role(A_PARTICIPANT)

        db_mock.session.commit.assert_called_once()


class TestRemoveOwnTeamRequest:
    A_TEAM_REQUEST = TeamRequest(team_id=A_TEAM.id, participant_id=A_PARTICIPANT_WITHOUT_TEAM.id)

    def test_given_no_team_request_should_raise_unprocessable_entity_error(self, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            teams.remove_own_team_request(A_PARTICIPANT)

    def test_should_delete_current_team_request(self, db_mock: MagicMock, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_REQUEST

        teams.remove_own_team_request(A_PARTICIPANT)

        db_mock.session.delete.assert_called_with(TeamRequest(team_id=self.A_TEAM_REQUEST.team_id,
                                                              participant_id=self.A_TEAM_REQUEST.participant_id))
        db_mock.session.commit.assert_called_once()


class TestLeaveTeam:
    A_TEAM_MEMBER = TeamMember(team_id=A_TEAM.id, participant_id=A_PARTICIPANT.id)

    def test_given_a_user_without_team_should_raise_unprocessable_entity_error(self,
                                                                               team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            teams.leave_team(A_PARTICIPANT)

    def test_should_delete_current_team_member(self,
                                               db_mock: MagicMock,
                                               team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_MEMBER

        teams.leave_team(A_PARTICIPANT)

        db_mock.session.delete.assert_called_with(TeamMember(team_id=self.A_TEAM_MEMBER.team_id,
                                                             participant_id=self.A_TEAM_MEMBER.participant_id))
        db_mock.session.commit.assert_called_once()
