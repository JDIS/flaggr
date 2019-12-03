"""Marshmallow schemas for the admin panel"""

from JDISCTF.schemas.admin.category import AdminCategorySchema, AdminCategoryRequestSchema
from JDISCTF.schemas.admin.challenge import AdminChallengeInformationSchema, AdminChallengeListSchema, \
    AdminChallengeRequestSchema, AdminChallengeSchema
from JDISCTF.schemas.admin.event import AdminEventListSchema, AdminEventSchema, AdminEventRequestSchema
from JDISCTF.schemas.admin.flag import FlagSchema