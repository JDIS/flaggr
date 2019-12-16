from copy import copy
from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.models import Administrator, Event, EventAdministrator
from JDISCTF.permission_wrappers import require_admin, require_admin_for_event, \
    require_admin_with_role


def local_patch(module: str):
    return patch('JDISCTF.permission_wrappers.' + module)


@fixture
def current_user_mock():
    with local_patch('current_user') as mock:
        yield mock


@fixture
def administrator_mock():
    with local_patch('Administrator') as mock:
        yield mock


AN_EVENT_ID = 1
AN_EVENT = Event(id=AN_EVENT_ID, name='', teams=True)
AN_ADMINISTRATOR = Administrator(id=0, is_platform_admin=True, user_id=0)

A_ROLE = 'role'


def has_current_administrator(*_, **kwargs):
    return 'current_admin' in kwargs


def NOP(*_, **__): pass


class TestRequireAdmin:
    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.get_administrator.return_value = AN_ADMINISTRATOR
        yield current_user_mock

    def test_given_user_without_administrator_should_raise_unauthorized(self, _current_user_mock: MagicMock):
        _current_user_mock.get_administrator.return_value = None

        with raises(errors.Unauthorized):
            require_admin(NOP)()

    def test_given_user_not_administering_event_should_raise_unauthorized(self, _current_user_mock: MagicMock):
        event = copy(AN_EVENT)
        event.id = AN_EVENT.id + 1
        admin = copy(AN_ADMINISTRATOR)
        admin.event_administrators = \
            [EventAdministrator(id=0, administrator_id=0, event_id=0, event=event)]
        _current_user_mock.get_administrator.return_value = admin

        with raises(errors.Unauthorized):
            require_admin_for_event(NOP)(event_id=AN_EVENT_ID)

    def test_given_user_administering_event_should_inject_current_participant(self, _current_user_mock: MagicMock):
        event = copy(AN_EVENT)
        event.id = AN_EVENT_ID
        admin = copy(AN_ADMINISTRATOR)
        admin.event_administrators = \
            [EventAdministrator(id=0, administrator_id=0, event_id=0, event=event)]
        _current_user_mock.get_administrator.return_value = admin

        assert require_admin_for_event(has_current_administrator)(event_id=AN_EVENT_ID)


class TestRequireAdminWithRole:
    @fixture(autouse=True)
    def _current_user_mock(self, current_user_mock: MagicMock):
        current_user_mock.get_administrator.return_value = AN_ADMINISTRATOR
        yield current_user_mock

    def test_given_user_without_administrator_should_raise_unauthorized(self, _current_user_mock: MagicMock):
        _current_user_mock.get_administrator.return_value = None

        with raises(errors.Unauthorized):
            require_admin_with_role(NOP, AN_EVENT_ID, '')()

    def test_given_user_not_administering_event_should_raise_unauthorized(self, _current_user_mock: MagicMock):
        event = copy(AN_EVENT)
        event.id = AN_EVENT.id + 1
        admin = copy(AN_ADMINISTRATOR)
        admin.event_administrators = \
            [EventAdministrator(id=0, administrator_id=0, event_id=0, event=event)]
        _current_user_mock.get_administrator.return_value = admin

        with raises(errors.Unauthorized):
            require_admin_with_role(NOP, AN_EVENT_ID, '')()

    def test_given_admin_without_required_role_should_raise_unauthorized(self,
                                                                         _current_user_mock: MagicMock,
                                                                         administrator_mock):
        event = copy(AN_EVENT)
        event.id = AN_EVENT_ID
        administrator_mock.events = [event]
        administrator_mock.get_roles_for_event.return_value = [A_ROLE]
        _current_user_mock.get_administrator.return_value = administrator_mock

        with raises(errors.Unauthorized):
            require_admin_with_role(has_current_administrator, AN_EVENT_ID, A_ROLE + 'a')()

    def test_given_user_with_role_administering_event_should_inject_current_participant(self,
                                                                                        _current_user_mock: MagicMock,
                                                                                        administrator_mock):
        event = copy(AN_EVENT)
        event.id = AN_EVENT_ID
        administrator_mock.events = [event]
        administrator_mock.get_roles_for_event.return_value = [A_ROLE]
        _current_user_mock.get_administrator.return_value = administrator_mock

        assert require_admin_with_role(has_current_administrator, AN_EVENT_ID, A_ROLE)
