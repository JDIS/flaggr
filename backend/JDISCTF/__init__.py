"""The JDIS ctf platform backend"""
# pylint: disable=invalid-name

# Make models available for sqlalchemy
from JDISCTF import models

# Import controllers for flask_rebar
from JDISCTF.api import auth, users
