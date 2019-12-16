from JDISCTF.api.admin.admin import get_connected_admin
from JDISCTF.api.admin.auth import login_administrator, register_administrator
from JDISCTF.api.admin.categories import create_category, get_admin_categories
from JDISCTF.api.admin.challenges import get_admin_challenges_for_event, get_admin_challenge, create_challenge,\
    edit_challenge, delete_challenge
from JDISCTF.api.admin.events import create_event, edit_event, delete_event, get_admin_events, get_admin_event