"""Marshmallow schemas for the admin panel"""

from JDISCTF.schemas.admin.category import AdminCategoryRequestSchema, AdminCategorySchema
from JDISCTF.schemas.admin.challenge import AdminChallengeListSchema, AdminChallengeRequestSchema, \
    AdminChallengeSchema
from JDISCTF.schemas.admin.event import AdminEventListSchema, AdminEventSchema, AdminEventRequestSchema
from JDISCTF.schemas.admin.flag import FlagSchema
