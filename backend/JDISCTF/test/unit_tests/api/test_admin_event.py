from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api.admin import events
from JDISCTF.models import Category, Challenge, Event, Flag, Submission, Team, User


def local_patch(module: str):
    return patch("JDISCTF.api.admin.events." + module)


@fixture
def event_mock():
    with local_patch("Event") as mock:
        yield mock


@fixture
def category_mock():
    with local_patch("Category") as mock:
        yield mock


@fixture
def challenge_mock():
    with local_patch("Challenge") as mock:
        yield mock


@fixture
def flag_mock():
    with local_patch("Flag") as mock:
        yield mock


@fixture
def rebar_mock():
    with local_patch("flask_rebar") as mock:
        yield mock


@fixture
def db_mock():
    with local_patch("DB") as mock:
        yield mock


@fixture
def current_user_mock():
    with local_patch("current_user") as mock:
        yield mock

A_CATEGORY = Category(id=0, event_id=0, name="Category")
A_EVENT = Event(id=0, name="Test Event", teams=True)
A_CHALLENGE = Challenge(id=0,name="Challenge name", points=100, hidden=False, description="My description", category_id=A_CATEGORY.id)
A_FLAG = Flag(id=None, challenge_id=A_CHALLENGE.id, is_regex=False, value="JDIS-FLAG")

class TestGetChallenge:
    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        yield db_mock

    @fixture(autouse=True)
    def _challenge_mock(self, challenge_mock: MagicMock):
        challenge_mock.side_effect = lambda *args, **kwargs: Challenge(*args, **kwargs)

    def test_given_non_existent_challenge_id_should_raise_not_found_error(self, challenge_mock: MagicMock, flag_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        flag_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.NotFound):
            challenges.get_admin_challenge(-1)

    def test_should_return_challenge(self, challenge_mock: MagicMock, flag_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = A_CHALLENGE
        flag_mock.query.filter_by.return_value.all.return_value = A_FLAG

        result = challenges.get_admin_challenge(1)
        assert result == {"challenge": A_CHALLENGE, "flags": A_FLAG}