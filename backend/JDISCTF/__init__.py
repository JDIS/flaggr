"""The JDIS ctf platform backend"""
# pylint: disable=invalid-name

# Make models available for sqlalchemy
from JDISCTF import models

# Import controllers for flask_rebar
from JDISCTF.api import auth, users, teams, challenges
from JDISCTF.app import create_app

from JDISCTF.permission_wrappers import require_participant
