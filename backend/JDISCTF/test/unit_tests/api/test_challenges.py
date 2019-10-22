from pytest import raises, fixture
from unittest.mock import MagicMock, patch
from flask_rebar import errors
from JDISCTF.api import get_challenge, get_all_challenges_for_event, \
    get_all_challenges_by_category_for_event
from JDISCTF.models import Challenge, Category


@fixture
def challenge_mock():
    with patch('JDISCTF.api.challenges.Challenge') as mock:
        yield mock


@fixture
def event_mock():
    with patch('JDISCTF.api.challenges.Event') as mock:
        yield mock


@fixture
def category_mock():
    with patch('JDISCTF.api.challenges.Category') as mock:
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

        challenge_mock.query\
            .join.return_value\
            .join.return_value\
            .filter.return_value\
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

        category_mock.query.options.return_value.filter_by.return_value.all.return_value = A_CATEGORY

        assert get_all_challenges_by_category_for_event(1) == A_CATEGORY
