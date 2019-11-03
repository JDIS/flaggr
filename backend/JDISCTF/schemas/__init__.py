"""Marshmallow schemas"""

from JDISCTF.schemas.challenge import UserChallengeSchema, ChallengeByCategorySchema,\
    SubmitFlagSchema, SubmitFlagResponseSchema
from JDISCTF.schemas.category import CategorySchema
from JDISCTF.schemas.user import CreateUserSchema, LoginSchema, LogoutSchema, UserSchema
