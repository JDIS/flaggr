"""Marshmallow schemas"""

from JDISCTF.schemas.category import CategorySchema
from JDISCTF.schemas.challenge import ChallengeByCategorySchema, SubmitFlagResponseSchema, \
    SubmitFlagSchema, UserChallengeSchema
from JDISCTF.schemas.user import CreateUserSchema, LoginSchema, LogoutSchema, UserSchema
