from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api.admin.auth import login_administrator, register_administrator
from JDISCTF.models import Administrator, User


def local_patch(module: str):
    return patch('JDISCTF.api.admin.auth.' + module)


@fixture
def flask_rebar_mock():
    with local_patch('flask_rebar') as mock:
        yield mock


@fixture
def user_mock():
    with local_patch('User') as mock:
        yield mock


A_USER = User(id=0, email="an_email", password_hash="a_password")
AN_ADMINISTRATOR = Administrator(id=0, is_platform_admin=False, user_id=0)


class TestLogin:

    @fixture(autouse=True)
    def _user_mock(self, user_mock: MagicMock):
        a_user_mock = MagicMock()
        a_user_mock.id = A_USER.id
        a_user_mock.email = A_USER.email
        a_user_mock.password_hash = A_USER.password_hash
        a_user_mock.check_password.return_value = True
        user_mock.query.filter_by.return_value.first.return_value = a_user_mock
        yield user_mock

    @fixture(autouse=True)
    def _flask_rebar_mock(self, flask_rebar_mock: MagicMock):
        flask_rebar_mock.get_validated_body.return_value = \
            {"email": "an_email", "password": "a_password", "remember": False}
        yield flask_rebar_mock

    @fixture(autouse=True)
    def login_user_mock(self):
        with local_patch('login_user') as mock:
            yield mock

    def test_given_invalid_email_should_raise_unprocessable_entity(self, user_mock: MagicMock):
        user_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            login_administrator()

    def test_given_invalid_password_should_raise_unprocessable_entity(self, _user_mock: MagicMock):
        a_user_mock = MagicMock()
        a_user_mock.check_password.return_value = False
        _user_mock.query.filter_by.return_value.first.return_value = a_user_mock

        with raises(errors.UnprocessableEntity):
            login_administrator()

    def test_given_credentials_not_for_administrator_should_raise_unauthorized(self, _user_mock: MagicMock):
        a_user_mock = MagicMock()
        a_user_mock.check_password.return_value = True
        a_user_mock.get_administrator.return_value = None
        _user_mock.query.filter_by.return_value.first.return_value = a_user_mock

        with raises(errors.Unauthorized):
            login_administrator()

    def test_should_login_user_with_flask_login(self, login_user_mock: MagicMock, _user_mock: MagicMock,
                                                _flask_rebar_mock: MagicMock):
        a_user_mock = MagicMock()
        a_user_mock.check_password.return_value = True
        _user_mock.query.filter_by.return_value.first.return_value = a_user_mock
        REMEMBER = True
        _flask_rebar_mock.get_validated_body.return_value = \
            {"email": "an_email", "password": "a_password", "remember": REMEMBER}

        login_administrator()

        login_user_mock.assert_called_with(a_user_mock, remember=REMEMBER)

    def test_should_return_logged_in_administrator(self, _user_mock: MagicMock):
        a_user_mock = MagicMock()
        a_user_mock.check_password.return_value = True
        a_user_mock.get_administrator.return_value = AN_ADMINISTRATOR
        _user_mock.query.filter_by.return_value.first.return_value = a_user_mock

        assert login_administrator() == AN_ADMINISTRATOR


class TestRegisterAdministrator:
    @fixture(autouse=True)
    def _flask_rebar_mock(self, flask_rebar_mock: MagicMock):
        flask_rebar_mock.get_validated_body.return_value = \
            {"email": "an_email", "password": "a_password", "username": "a_username"}
        yield flask_rebar_mock

    @fixture(autouse=True)
    def _user_mock(self, user_mock: MagicMock):
        user_mock.query.filter_by.return_value.first.return_value = None
        yield user_mock

    @fixture(autouse=True)
    def db_mock(self):
        with local_patch('DB') as mock:
            yield mock

    @fixture(autouse=True)
    def administrator_mock(self):
        with local_patch('Administrator') as mock:
            yield mock

    def test_given_admin_with_email_already_existing_should_raise_unprocessable_entity(self, user_mock: MagicMock):
        a_user_mock = MagicMock()
        a_user_mock.get_administrator.return_value = AN_ADMINISTRATOR
        user_mock.query.filter_by.return_value.first.return_value = a_user_mock

        with raises(errors.UnprocessableEntity):
            register_administrator()

    def test_given_admin_with_username_already_existing_should_raise_unprocessable_entity(self, user_mock: MagicMock):
        def side_effect(**kwargs):
            mock = MagicMock()
            if "email" in kwargs:
                mock.first.return_value = None
            elif "username" in kwargs:
                a_user_mock = MagicMock()
                a_user_mock.get_administrator.return_value = AN_ADMINISTRATOR
                mock.first.return_value = a_user_mock

            return mock

        user_mock.query.filter_by.side_effect = side_effect

        with raises(errors.UnprocessableEntity):
            register_administrator()

    def test_should_set_user_password(self, user_mock: MagicMock, _flask_rebar_mock: MagicMock):
        A_PASSWORD = "a_password"
        _flask_rebar_mock.get_validated_body.return_value["password"] = A_PASSWORD
        a_user_mock = MagicMock()
        user_mock.side_effect = lambda **_: a_user_mock

        register_administrator()

        a_user_mock.set_password.assert_called_with(A_PASSWORD)

    def test_should_add_and_commit_new_administrator(self, db_mock: MagicMock, administrator_mock: MagicMock):
        administrator_mock.side_effect = lambda **_: AN_ADMINISTRATOR

        register_administrator()

        db_mock.session.add.assert_called_with(AN_ADMINISTRATOR)
        db_mock.session.commit.assert_called_once()

    def test_should_return_new_administrator_with_code_201(self, administrator_mock: MagicMock):
        administrator_mock.side_effect = lambda **_: AN_ADMINISTRATOR
        assert register_administrator() == (AN_ADMINISTRATOR, 201)
