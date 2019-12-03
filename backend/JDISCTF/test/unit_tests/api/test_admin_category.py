from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api.admin import categories
from JDISCTF.models import Category, Challenge, Event, Flag, Submission, Team, User


def local_patch(module: str):
    return patch("JDISCTF.api.admin.categories." + module)


@fixture
def event_mock():
    with local_patch("Event") as mock:
        yield mock


@fixture
def category_mock():
    with local_patch("Category") as mock:
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

A_CATEGORY = Category(id=None, event_id=1, name="Category")
A_EVENT = Event(id=0, name="Test Event", teams=True)

class TestCreateCategory:
    REQUEST_BODY = {"event_id": 0, "name": "New Category"}
    A_NEW_CATEGORY = Category(id=None, event_id=REQUEST_BODY["event_id"], name=REQUEST_BODY["name"])

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        yield db_mock

    @fixture(autouse=True)
    def _event_mock(self, event_mock: MagicMock):
        yield event_mock

    @fixture(autouse=True)
    def _category_mock(self, category_mock: MagicMock):
        category_mock.side_effect = lambda *args, **kwargs: Category(*args, **kwargs)

    def test_given_non_existent_event_id_should_raise_not_found_error(self, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = None
        with raises(errors.NotFound):
            categories.create_category()
    
    def test_given_already_used_name_should_raise_not_found_error(self, category_mock: MagicMock):
        category_mock.query.filter_by.return_value.first.return_value = A_CATEGORY

        with raises(errors.UnprocessableEntity):
            categories.create_category()

    def test_given_should_create_a_category(self, category_mock: MagicMock, db_mock: MagicMock):
        category_mock.query.filter_by.return_value.first.return_value = None

        categories.create_category()

        db_mock.session.add.assert_called_with(self.A_NEW_CATEGORY)
        db_mock.session.commit.assert_called_once()

    def test_given_should_return_category(self, category_mock: MagicMock, db_mock: MagicMock):
        category_mock.query.filter_by.return_value.first.return_value = None

        result = categories.create_category()

        assert result == self.A_NEW_CATEGORY