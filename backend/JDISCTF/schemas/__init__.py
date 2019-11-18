"""Marshmallow schemas"""

from JDISCTF.schemas.category import CategorySchema
from JDISCTF.schemas.challenge import ChallengeByCategorySchema, SubmitFlagResponseSchema, \
    SubmitFlagSchema, UserChallengeSchema
from JDISCTF.schemas.team import AcceptTeamRequestRequestSchema, \
    ChangeRoleRequestSchema, CreateTeamRequestSchema, DeclineTeamRequestRequestSchema, \
    KickTeamMemberRequestSchema, SendTeamRequestRequestSchema, TeamRequestSchema, \
    TeamSchema
from JDISCTF.schemas.user import CreateUserSchema, LoginSchema, UserSchema, ParticipantSchema
from JDISCTF.schemas.generic import GenericMessageSchema
from JDISCTF.schemas.participant import ParticipantSchema
