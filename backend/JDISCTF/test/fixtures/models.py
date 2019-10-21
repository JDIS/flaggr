from unittest.mock import patch
from pytest import fixture


@fixture
def challenge_mock():
    with patch('JDISCTF.api.challenges.Challenge') as mock:
        yield mock
