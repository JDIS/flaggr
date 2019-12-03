from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api.admin import events
from JDISCTF.models import Event


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

A_EVENT = Event(id=0, name="Test Event", teams=True)