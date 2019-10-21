from pytest import raises
from unittest.mock import MagicMock
from flask_rebar import errors
from JDISCTF.api import get_challenge
from JDISCTF.models import Challenge
from JDISCTF.test.fixtures import challenge_mock


class TestGetChallenge:
    def test_given_non_existent_challenge_id_should_raise_not_found_error(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        with raises(errors.NotFound):
            get_challenge(1)

    def test_given_existent_challenge_id_should_return_challenge(self, challenge_mock: MagicMock):
        a_challenge = Challenge(id=1, category_id=1, name='Challenge', description='Description',
                                points=100, hidden=False)
        challenge_mock.query.filter_by.return_value.first.return_value = a_challenge

        assert get_challenge(a_challenge.id) == a_challenge
