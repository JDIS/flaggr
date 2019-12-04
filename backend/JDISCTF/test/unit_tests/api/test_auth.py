from unittest.mock import MagicMock, patch

from pytest import fixture

from JDISCTF.api import logout


def local_patch(module: str):
    return patch('JDISCTF.api.auth.' + module)


class TestLogout:
    @fixture(autouse=True)
    def logout_user_mock(self):
        with local_patch('logout_user') as mock:
            yield mock

    def test_should_logout_user_with_flask_login(self, logout_user_mock: MagicMock):
        logout()

        logout_user_mock.assert_called_once()
