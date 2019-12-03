"""API routes for the application"""

from JDISCTF.api.admin.categories import create_category, get_admin_categories
from JDISCTF.api.admin.challenges import get_admin_challenges, get_admin_challenge

from JDISCTF.api.auth import register_participant
from JDISCTF.api.challenges import get_all_challenges_by_category_for_event, \
    get_all_challenges_for_event, \
    get_challenge, submit_flag
from JDISCTF.api.events import get_all_events, get_event
from JDISCTF.api.scoreboard import get_scoreboard
from JDISCTF.api.teams import accept_team_request, change_role, create_team, current_team, \
    decline_team_request, \
    get_team_request, kick_team_member, leave_team, remove_own_team_request, send_team_request, \
    teams_list
from JDISCTF.api.users import get_user
from JDISCTF.api.participants import get_connected_participant
