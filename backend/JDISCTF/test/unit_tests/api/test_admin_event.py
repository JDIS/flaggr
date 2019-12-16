import inspect
from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api.admin import events
from JDISCTF.models import Administrator, Event


def local_patch(module: str):
    return patch("JDISCTF.api.admin.events." + module)


@fixture
def event_mock():
    with local_patch("Event") as mock:
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

A_EVENT = Event(id=0, name="Test Event", teams=True, is_open=False)
AN_ADMINISTRATOR = Administrator(id=0, is_platform_admin=True, user_id=0)

class TestCreateEvent:
    REQUEST_BODY = {"name": "Test Event", "teams": True, "is_open": False, "is_visible": False, "front_page": "", "flag_format": ""}
    A_NEW_EVENT = Event(name=REQUEST_BODY["name"], teams=REQUEST_BODY["teams"], is_open=REQUEST_BODY["is_open"], is_visible=REQUEST_BODY["is_visible"],
                        front_page=REQUEST_BODY["front_page"], flag_format=REQUEST_BODY["flag_format"])

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _event_mock(self, event_mock: MagicMock):
        event_mock.side_effect = lambda *args, **kwargs: Event(*args, **kwargs)


    def test_givent_an_already_existing_name_should_raise_unprocessable_entity(self, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = A_EVENT

        with raises(errors.UnprocessableEntity):
            inspect.unwrap(events.create_event)(AN_ADMINISTRATOR)


    def test_should_create_event(self, db_mock: MagicMock, event_mock: MagicMock):
        event_mock.query.filter_by.return_value.first.return_value = None

        inspect.unwrap(events.create_event)(AN_ADMINISTRATOR)

        db_mock.session.add.assert_called_with(self.A_NEW_EVENT)
        db_mock.session.commit.assert_called_once()
