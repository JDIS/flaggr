"""API routes for the application"""

from JDISCTF.api.auth import register
from JDISCTF.api.teams import accept_team_request, create_team, current_team, kick_team_member,\
    leave_team
from JDISCTF.api.challenges import get_all_challenges_by_category_for_event, \
    get_all_challenges_for_event, get_challenge, submit_flag
from JDISCTF.api.users import get_user
