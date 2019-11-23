from datetime import datetime
from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api import accept_team_request, change_role, create_team, current_team, decline_team_request, \
    kick_team_member, leave_team, remove_own_team_request, send_team_request, teams_list
from JDISCTF.models import Event, Team, TeamMember, TeamRequest, User


def local_patch(module: str):
    return patch('JDISCTF.api.teams.' + module)


@fixture
def challenge_mock():
    with local_patch('Challenge') as mock:
        yield mock


@fixture
def category_mock():
    with local_patch('Category') as mock:
        yield mock


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


@fixture
def current_user_mock():
    with local_patch('current_user') as mock:
        yield mock


A_EVENT = Event(id=0, name="Test Event", teams=True)

A_USER = User(id=0, username="test", email="test@gmail.com", event_id=A_EVENT.id)
A_USER.set_password("test")

A_USER_WITHOUT_TEAM = User(id=1, username="test2", email="test2@gmail.com", event_id=A_EVENT.id)
A_USER_WITHOUT_TEAM.set_password("test2")

A_USER_NOT_CAPTAIN = User(id=2, username="test3", email="test3@gmail.com", event_id=A_EVENT.id)
A_USER_NOT_CAPTAIN.set_password("test3")

A_TEAM = Team(id=0, name="Test Team", event_id=A_EVENT.id,
              members=[TeamMember(user_id=A_USER.id, captain=True),
                       TeamMember(user_id=A_USER_NOT_CAPTAIN.id, captain=False)])


class TestCurrentTeam:
    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.return_value = A_USER
        yield current_user_mock

    def test_given_a_user_without_a_team(self, _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = None
        result = current_team()

        assert result is None

    def test_given_a_user_with_a_team(self, _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        result = current_team()

        assert result == A_TEAM


class TestTeamsList:
    def test_should_return_all_lists_for_event(self, team_mock):
        team_mock.query.filter_by.return_value.join.return_value.all.return_value = [A_TEAM]
        teams = teams_list()
        assert teams == [A_TEAM]


class TestCreateTeam:
    REQUEST_BODY = {"team_name": "Test Team"}

    A_NEW_TEAM = Team(id=None, name=REQUEST_BODY["team_name"], event_id=A_USER_WITHOUT_TEAM.event_id,
                      members=[TeamMember(user_id=A_USER_WITHOUT_TEAM.id, captain=True)])

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.id = A_USER_WITHOUT_TEAM.id
        current_user_mock.event_id = A_USER_WITHOUT_TEAM.event_id
        current_user_mock.get_team.return_value = None
        yield current_user_mock

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
                                                                                    _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM

        with raises(errors.UnprocessableEntity):
            create_team()

    def test_given_an_already_existing_team_name_should_raise_unprocessable_entity_error(self,
                                                                                         team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = A_TEAM

        with raises(errors.UnprocessableEntity):
            create_team()

    def test_should_create_a_team(self, db_mock: MagicMock, team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = None

        create_team()

        db_mock.session.add.assert_called_with(self.A_NEW_TEAM)

        db_mock.session.commit.assert_called_once()

    def test_should_return_created_team(self, team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = None
        team = create_team()
        assert team == self.A_NEW_TEAM


class TestGetTeamRequest:
    def test_should_return_current_user_team_request(self, team_request_mock: MagicMock):
        a_team_request = TeamRequest(id=0, user_id=1, team_id=2, requested_at=datetime.now())
        result = team_request_mock.query.filter_by.return_value.first.return_value = a_team_request
        assert result == a_team_request


class TestSendTeamRequest:
    A_TEAM_REQUEST = TeamRequest(user_id=A_USER_WITHOUT_TEAM.id, team_id=A_TEAM.id)
    REQUEST_BODY = {"team_id": A_TEAM_REQUEST.team_id}

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.id = A_USER_WITHOUT_TEAM.id
        current_user_mock.event_id = A_USER_WITHOUT_TEAM.event_id
        current_user_mock.get_team.return_value = None

        yield current_user_mock

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
                                                                                    _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM

        with raises(errors.UnprocessableEntity):
            send_team_request()

    def test_given_an_non_existent_team_id_should_raise_unprocessable_entity_error(self,
                                                                                   team_mock: MagicMock):
        team_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            send_team_request()

    def test_given_a_user_with_team_request_should_raise_unprocessable_entity_error(self, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value \
            = {"user_id": A_USER_WITHOUT_TEAM.id, "team_id": A_TEAM.id}

        with raises(errors.UnprocessableEntity):
            send_team_request()

    def test_should_send_team_request(self, db_mock: MagicMock, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value = None

        send_team_request()

        db_mock.session.add.assert_called_with(TeamRequest(user_id=self.A_TEAM_REQUEST.user_id,
                                                           team_id=self.A_TEAM_REQUEST.team_id))
        db_mock.session.commit.assert_called_once()


class TestAcceptTeamRequest:
    A_TEAM_REQUEST = TeamRequest(team_id=A_TEAM.members[0].team_id, user_id=A_USER_WITHOUT_TEAM.id)
    A_TEAM_MEMBER = TeamMember(team_id=A_TEAM.members[0].team_id, user_id=A_USER_WITHOUT_TEAM.id)
    REQUEST_BODY = {"user_id": A_TEAM_REQUEST.user_id}

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        yield current_user_mock

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
            accept_team_request()

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = A_TEAM.members[1]

        with raises(errors.Unauthorized):
            accept_team_request()

    def test_given_an_invalid_user_id_should_raise_unprocessable_entity_error(self,
                                                                              team_member_mock: MagicMock,
                                                                              team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = A_TEAM.members[0]
        team_request_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            accept_team_request()

    def test_should_delete_team_request_and_add_user_to_team(self,
                                                             db_mock: MagicMock,
                                                             team_member_mock: MagicMock,
                                                             team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = A_TEAM.members[0]
        team_request_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_REQUEST

        accept_team_request()

        db_mock.session.delete.assert_called_with(
            TeamRequest(user_id=self.A_TEAM_REQUEST.user_id, team_id=self.A_TEAM_REQUEST.team_id))
        db_mock.session.add.assert_called_with(
            TeamMember(user_id=self.A_TEAM_MEMBER.user_id, team_id=self.A_TEAM_MEMBER.team_id))
        db_mock.session.commit.assert_called_once()


class TestDeclineTeamRequest:
    A_TEAM_REQUEST = TeamRequest(team_id=A_TEAM.members[0].team_id, user_id=A_USER_WITHOUT_TEAM.id)
    REQUEST_BODY = {"user_id": A_TEAM_REQUEST.user_id}

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        yield current_user_mock

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY

        yield rebar_mock

    def test_given_a_user_without_team_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.Unauthorized):
            decline_team_request()

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value =\
            TeamMember(user_id=A_USER_NOT_CAPTAIN.id, captain=False)

        with raises(errors.Unauthorized):
            decline_team_request()

    def test_given_an_invalid_user_id_should_raise_unprocessable_entity_error(self,
                                                                              team_member_mock: MagicMock,
                                                                              team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(user_id=A_USER.id, captain=True)
        team_request_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            decline_team_request()

    def test_should_delete_team_request(self,
                                        db_mock: MagicMock,
                                        team_member_mock: MagicMock,
                                        team_request_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(user_id=A_USER.id, captain=True)
        team_request_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_REQUEST

        decline_team_request()

        db_mock.session.delete.assert_called_with(TeamRequest(user_id=self.A_TEAM_REQUEST.user_id,
                                                              team_id=self.A_TEAM_REQUEST.team_id))
        db_mock.session.commit.assert_called_once()


class TestKickTeamMember:
    A_TEAM_MEMBER = TeamMember(team_id=A_TEAM.id, user_id=A_USER_NOT_CAPTAIN.id)
    REQUEST_BODY = {"user_id": A_TEAM_MEMBER.user_id}

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.id = A_USER.id
        yield current_user_mock

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
            kick_team_member()

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value =\
            TeamMember(user_id=A_USER_NOT_CAPTAIN.id, captain=False)

        with raises(errors.Unauthorized):
            kick_team_member()

    def test_given_the_current_user_id_should_raise_unprocessable_entity_error(self,
                                                                               team_member_mock: MagicMock,
                                                                               _rebar_mock: MagicMock):
        _rebar_mock.get_validated_body.return_value = {"user_id": A_USER.id}
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(user_id=A_USER.id, captain=True)

        with raises(errors.UnprocessableEntity):
            kick_team_member()

    def test_should_delete_team_member(self, db_mock: MagicMock, team_member_mock: MagicMock):
        # Multiple call needs to return different things
        team_member_mock.query.filter_by.return_value.first.side_effect = \
            [TeamMember(user_id=A_USER.id, captain=True), self.A_TEAM_MEMBER]

        kick_team_member()

        db_mock.session.delete.assert_called_with(TeamMember(user_id=self.A_TEAM_MEMBER.user_id,
                                                             team_id=self.A_TEAM_MEMBER.team_id))
        db_mock.session.commit.assert_called_once()


class TestChangeRole:
    REQUEST_BODY = {"user_id": A_USER_NOT_CAPTAIN.id, "captain": True}

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.id = A_USER.id
        yield current_user_mock

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    def test_given_a_user_without_team_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.Unauthorized):
            change_role()

    def test_given_a_non_captain_should_raise_unauthorized_error(self, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value =\
            TeamMember(user_id=A_USER_NOT_CAPTAIN.id, captain=False)

        with raises(errors.Unauthorized):
            change_role()

    def test_given_the_current_user_id_should_raise_unprocessable_entity_error(self,
                                                                               team_member_mock: MagicMock,
                                                                               _rebar_mock: MagicMock):
        _rebar_mock.get_validated_body.return_value = {"user_id": A_USER.id, "captain": True}
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(user_id=A_USER.id, captain=True)

        with raises(errors.UnprocessableEntity):
            change_role()

    def test_should_commit_changes(self, db_mock: MagicMock, team_member_mock: MagicMock):
        team_member_mock.query.filter_by.return_value.first.return_value = TeamMember(user_id=A_USER.id, captain=True)

        change_role()

        db_mock.session.commit.assert_called_once()


class TestRemoveOwnTeamRequest:
    A_TEAM_REQUEST = TeamRequest(team_id=A_TEAM.id, user_id=A_USER_WITHOUT_TEAM.id)

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.return_value = A_USER_WITHOUT_TEAM
        yield current_user_mock

    def test_given_no_team_request_should_raise_unprocessable_entity_error(self, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            remove_own_team_request()

    def test_should_delete_current_team_request(self, db_mock: MagicMock, team_request_mock: MagicMock):
        team_request_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_REQUEST

        remove_own_team_request()

        db_mock.session.delete.assert_called_with(TeamRequest(team_id=self.A_TEAM_REQUEST.team_id,
                                                              user_id=self.A_TEAM_REQUEST.user_id))
        db_mock.session.commit.assert_called_once()


class TestLeaveTeam:
    A_TEAM_MEMBER = TeamMember(team_id=A_TEAM.id, user_id=A_USER.id)

    def test_given_a_user_without_team_should_raise_unprocessable_entity_error(self,
                                                                               current_user_mock: MagicMock,
                                                                               team_member_mock: MagicMock):
        current_user_mock.return_value = A_USER_WITHOUT_TEAM
        team_member_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            leave_team()

    def test_should_delete_current_team_member(self,
                                               db_mock: MagicMock,
                                               current_user_mock: MagicMock,
                                               team_member_mock: MagicMock):
        current_user_mock.return_value = A_USER
        team_member_mock.query.filter_by.return_value.first.return_value = self.A_TEAM_MEMBER

        leave_team()

        db_mock.session.delete.assert_called_with(TeamMember(team_id=self.A_TEAM_MEMBER.team_id,
                                                             user_id=self.A_TEAM_MEMBER.user_id))
        db_mock.session.commit.assert_called_once()
