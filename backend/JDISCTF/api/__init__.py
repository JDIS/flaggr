"""API routes for the application"""

from JDISCTF.api.auth import register
from JDISCTF.api.users import get_user
from JDISCTF.api.challenges import get_all_challenges_for_event, get_challenge,\
    get_all_challenges_by_category_for_event
