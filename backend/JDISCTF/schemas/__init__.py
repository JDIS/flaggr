"""Marshmallow schemas"""

from JDISCTF.schemas.category import CategorySchema
from JDISCTF.schemas.challenge import ChallengeByCategorySchema, SubmitFlagResponseSchema, \
    SubmitFlagSchema, UserChallengeSchema
from JDISCTF.schemas.team import CreateTeamRequestSchema, JoinRequestSchema, JoinTeamRequestSchema,\
    TeamSchema
from JDISCTF.schemas.user import CreateUserSchema, LoginSchema, LogoutSchema, UserSchema
from JDISCTF.schemas.generic import GenericMessageSchema