from pytest import raises, fixture
from unittest.mock import MagicMock, patch
from flask_rebar import errors
from JDISCTF.api import get_challenge, get_all_challenges_for_event, \
    get_all_challenges_by_category_for_event, submit_flag
from JDISCTF.models import Challenge, Category, Team, Submission, Flag


def local_patch(module: str):
    return patch('JDISCTF.api.challenges.' + module)


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
def team_mock():
    with local_patch('Team') as mock:
        yield mock


@fixture
def rebar_mock():
    with local_patch('flask_rebar') as mock:
        yield mock


@fixture
def db_mock():
    with local_patch('DB') as mock:
        yield mock


A_CHALLENGE = Challenge(id=1, category_id=1, name='Challenge', description='Description',
                        points=100, hidden=False)
A_CATEGORY = Category(id=1, event_id=1, name='Category')


class TestGetAllChallengesForEvent:
    def test_given_non_existent_event_id_should_raise_not_found_error(self, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = None
        with raises(errors.NotFound):
            get_all_challenges_for_event(1)

    def test_should_return_challenges(self, challenge_mock: MagicMock, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = 1

        challenge_mock.query \
            .join.return_value \
            .join.return_value \
            .filter.return_value \
            .all.return_value = [A_CHALLENGE]

        assert get_all_challenges_for_event(1) == [A_CHALLENGE]


class TestGetChallenge:
    def test_given_non_existent_challenge_id_should_raise_not_found_error(self,
                                                                          challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        with raises(errors.NotFound):
            get_challenge(1)

    def test_should_return_challenge(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = A_CHALLENGE

        assert get_challenge(A_CHALLENGE.id) == A_CHALLENGE


class TestGetChallengesByCategoryForEvent:
    def test_given_non_existent_event_id_should_raise_not_found_error(self, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.NotFound):
            get_all_challenges_by_category_for_event(1)

    def test_should_return_challenges(self, event_mock: MagicMock, category_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = 1

        category_mock.query.join.return_value.options.return_value.filter.return_value \
            .all.return_value = A_CATEGORY

        assert get_all_challenges_by_category_for_event(1) == A_CATEGORY


class TestSubmitFlag:
    EVENT_ID = 1
    A_TEAM = Team(id=1, event_id=EVENT_ID, name='Team 1')
    REQUEST_BODY = {"team_id": 1, "flag": "JDIS"}

    @fixture(autouse=True)
    def _challenge_mock(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = A_CHALLENGE
        yield challenge_mock

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _team_mock(self, team_mock: MagicMock):
        team_mock.query.get.return_value = self.A_TEAM
        yield team_mock

    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        # Mock the event id the challenge belongs to
        db_mock.session.query.return_value.join.return_value.filter.return_value.first.return_value = (self.EVENT_ID,)
        yield db_mock

    @fixture(autouse=True)
    def flag_mock(self):
        with local_patch('Flag') as mock:
            yield mock

    def test_given_non_existent_challenge_id_should_raise_not_found_error(self,
                                                                          _challenge_mock: MagicMock):
        _challenge_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.NotFound):
            submit_flag(1)

    def test_given_non_existent_team_id_should_raise_not_found_error(self,
                                                                     _team_mock: MagicMock):
        _team_mock.query.get.return_value = None

        with raises(errors.NotFound):
            submit_flag(1)

    def test_given_challenge_and_team_not_in_same_event_should_raise_unprocessable_entity_error(self,
                                                                                       _team_mock: MagicMock,
                                                                                       _db_mock: MagicMock):
        challenge_event_id = 1
        team_in_other_event = Team(id=1, event_id=challenge_event_id + 1, name='Team 1')

        # Mock the event id the challenge belongs to
        _db_mock.session.query.return_value.join.return_value.filter.return_value.first.return_value = (challenge_event_id,)

        _team_mock.query.get.return_value = team_in_other_event

        with raises(errors.UnprocessableEntity):
            submit_flag(1)

    def test_given_correct_non_regex_flag_should_persist_submission_with_is_correct_true(self,
                                                                                         _db_mock: MagicMock,
                                                                                         flag_mock: MagicMock):
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=False,
                                                                        value=self.REQUEST_BODY['flag'])]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=self.A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=True))

    def test_given_correct_regex_flag_should_persist_submission_with_is_correct_true(self,
                                                                                     _db_mock: MagicMock,
                                                                                     flag_mock: MagicMock):
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY['flag'])]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=self.A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=True))

    def test_given_non_correct_non_regex_flag_should_persist_submission_with_is_correct_true(self,
                                                                                             _db_mock: MagicMock,
                                                                                             flag_mock: MagicMock):
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=False,
                                                                        value=self.REQUEST_BODY['flag'] + '1')]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=self.A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=False))
        _db_mock.session.commit.assert_called_once()

    def test_given_non_correct_regex_flag_should_persist_submission_with_is_correct_true(self,
                                                                                         _db_mock: MagicMock,
                                                                                         flag_mock: MagicMock):
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY['flag'] + '1')]

        submit_flag(1)

        _db_mock.session.add.assert_called_with(Submission(team_id=self.A_TEAM.id,
                                                           challenge_id=A_CHALLENGE.id,
                                                           input=self.REQUEST_BODY['flag'],
                                                           is_correct=False))

    def test_given_correct_flag_should_return_correct_true(self, flag_mock: MagicMock):
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY['flag'])]

        result = submit_flag(1)
        assert result == {'correct': True}

    def test_given_incorrect_flag_should_return_correct_false(self, flag_mock: MagicMock):
        flag_mock.query.filter_by.return_value.all.return_value = [Flag(id=1,
                                                                        challenge_id=A_CHALLENGE.id,
                                                                        is_regex=True,
                                                                        value=self.REQUEST_BODY[
                                                                            'flag'] + '1')]

        result = submit_flag(1)
        assert result == {'correct': False}
