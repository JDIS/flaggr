from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api import get_all_challenges_by_category_for_event, get_all_challenges_for_event, \
    get_challenge, \
    submit_flag
from JDISCTF.models import Category, Challenge, Event, Flag, Submission, Team, User

EVENT_ID = 1
A_TEAM = Team(id=1, event_id=EVENT_ID, name='Team 1')
REQUEST_BODY = {"team_id": 1, "flag": "JDIS"}
A_EVENT = Event(id=0, name="Test Event", teams=True)
A_USER = User(id=0, username="test", email="test@gmail.com")


def local_patch(module: str):
    return patch('JDISCTF.api.challenges.' + module)


@fixture(autouse=True)
def require_event_mock():
    with patch('JDISCTF.permission_wrappers.Event') as mock:
        yield mock


@fixture
def challenge_mock():
    with local_patch('Challenge') as mock:
        yield mock


@fixture
def event_mock():
    with local_patch('Event') as mock:
        yield mock


@fixture
def category_mock():
    with local_patch('Category') as mock:
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


@fixture
def submission_mock():
    with local_patch('Submission') as mock:
        yield mock

A_CHALLENGE = Challenge(id=1, category_id=1, name='Challenge', description='Description',
                        points=100, hidden=False)
A_CATEGORY = Category(id=1, event_id=1, name='Category')


class TestGetAllChallengesForEvent:

    @fixture(autouse=True)
    def _submission_mock(self, submission_mock: MagicMock):
        submission_mock.query.filter.return_value.exists.return_value.label.return_value = 1
        yield submission_mock

    @fixture(autouse=True)
    def _event_mock(self, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = 1
        yield event_mock

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.return_value = A_USER
        yield current_user_mock

    def test_given_non_existent_event_id_should_raise_not_found_error(self, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = None
        with raises(errors.NotFound):
            get_all_challenges_for_event(1)

    def test_should_return_challenges(self, db_mock: MagicMock):
        return_value = MagicMock()
        return_value.Challenge = A_CHALLENGE

        db_mock.session.query.return_value \
            .join.return_value \
            .join.return_value \
            .filter.return_value \
            .all.return_value = [return_value]

        assert list(get_all_challenges_for_event(1)) == [A_CHALLENGE]

    def test_should_assign_completed(self, db_mock: MagicMock):
        return_value = MagicMock()
        return_value.Challenge = A_CHALLENGE
        return_value.__getitem__.return_value = True

        db_mock.session.query.return_value \
            .join.return_value \
            .join.return_value \
            .filter.return_value \
            .all.return_value = [return_value]

        assert list(get_all_challenges_for_event(1))[0].completed == True


class TestGetChallenge:

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.return_value = A_USER
        yield current_user_mock

    @fixture(autouse=True)
    def _submission_mock(self, submission_mock: MagicMock):
        submission_mock.query.filter.return_value.exists.return_value.label.return_value = 1
        yield submission_mock

    def test_given_non_existent_challenge_id_should_raise_not_found_error(self, db_mock: MagicMock,
                                                                          _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        db_mock.session.query.return_value.filter_by.return_value.first.return_value = None
        with raises(errors.NotFound):
            get_challenge(1)

    def test_should_return_challenge(self, db_mock: MagicMock):
        return_value = MagicMock()
        return_value.Challenge = A_CHALLENGE

        db_mock.session.query.return_value.filter_by.return_value.first.return_value = return_value

        assert get_challenge(A_CHALLENGE.id) == A_CHALLENGE

    def test_should_assign_completed(self, db_mock):
        return_value = MagicMock()
        return_value.Challenge = A_CHALLENGE
        return_value.__getitem__.return_value = True

        db_mock.session.query.return_value.filter_by.return_value.first.return_value = return_value

        assert get_challenge(A_CHALLENGE.id).completed == True


class TestGetChallengesByCategoryForEvent:
    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.return_value = A_USER
        yield current_user_mock

    def test_given_non_existent_event_id_should_raise_not_found_error(self, require_event_mock: MagicMock):
        require_event_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.NotFound):
            get_all_challenges_by_category_for_event(event_id=1)

    def test_should_return_challenges(self, event_mock: MagicMock, category_mock: MagicMock,
                                      _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        event_mock.query.filter_by.return_value.first.return_value = 1

        category_mock.query\
            .join.return_value\
            .options.return_value\
            .filter.return_value \
            .all.return_value = [A_CATEGORY]

        assert get_all_challenges_by_category_for_event(event_id=1) == [A_CATEGORY]


class TestSubmitFlag:
    REQUEST_BODY = {"team_id": 1, "flag": "JDIS"}

    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.return_value = A_USER
        yield current_user_mock

    @fixture(autouse=True)
    def _challenge_mock(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = A_CHALLENGE
        yield challenge_mock

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        # Mock the event id the challenge belongs to
        db_mock.session.query.return_value.join.return_value.filter.return_value.first.return_value = (EVENT_ID,)
        yield db_mock

    @fixture(autouse=True)
    def flag_mock(self):
        with local_patch('Flag') as mock:
            yield mock

    def test_given_non_existent_challenge_id_should_raise_not_found_error(self,
                                                                          _challenge_mock: MagicMock,
                                                                          _current_user_mock: MagicMock):
        _challenge_mock.query.filter_by.return_value.first.return_value = None
        _current_user_mock.get_team.return_value = A_TEAM

        with raises(errors.NotFound):
            submit_flag(1)

    def test_given_non_existent_team_id_should_raise_not_found_error(self,
                                                                     _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = None

        with raises(errors.NotFound):
            submit_flag(1)

    def test_given_challenge_and_team_not_in_same_event_should_raise_unprocessable_entity_error(self,
                                                                                       _db_mock: MagicMock,
                                                                                       _current_user_mock: MagicMock):
        challenge_event_id = 1
        team_in_other_event = Team(id=1, event_id=challenge_event_id + 1, name='Team 1')

        # Mock the event id the challenge belongs to
        _db_mock.session.query.return_value.join.return_value.filter.return_value.first.return_value = (challenge_event_id,)

        _current_user_mock.get_team.return_value = team_in_other_event

        with raises(errors.UnprocessableEntity):
            submit_flag(1)

    def test_given_correct_non_regex_flag_should_persist_submission_with_is_correct_true(self,
                                                                                         _db_mock: MagicMock,
                                                                                         flag_mock: MagicMock,
                                                                                 _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM

        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=False,
                                                                        value=self.REQUEST_BODY['flag'])]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=True))

    def test_given_correct_regex_flag_should_persist_submission_with_is_correct_true(self,
                                                                                     _db_mock: MagicMock,
                                                                                     flag_mock: MagicMock,
                                                                                     _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY['flag'])]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=True))

    def test_given_non_correct_non_regex_flag_should_persist_submission_with_is_correct_true(self,
                                                                                             _db_mock: MagicMock,
                                                                                             flag_mock: MagicMock,
                                                                                         _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=False,
                                                                        value=self.REQUEST_BODY['flag'] + '1')]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=False))
        _db_mock.session.commit.assert_called_once()

    def test_given_non_correct_regex_flag_should_persist_submission_with_is_correct_false(self,
                                                                                         _db_mock: MagicMock,
                                                                                         flag_mock: MagicMock,
                                                                                         _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY['flag'] + '1')]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=False))

    def test_given_correct_flag_should_return_correct_true(self, flag_mock: MagicMock,
                                                           _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY['flag'])]

        result = submit_flag(1)
        assert result == {'correct': True}

    def test_given_incorrect_flag_should_return_correct_false(self, flag_mock: MagicMock,
                                                              _current_user_mock: MagicMock):
        _current_user_mock.get_team.return_value = A_TEAM
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY[
                                                                            'flag'] + '1')]

        result = submit_flag(1)
        assert result == {'correct': False}
