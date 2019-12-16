from JDISCTF.api.admin.admin import get_connected_admin
from JDISCTF.api.admin.auth import login_administrator, register_administrator
from JDISCTF.api.admin.categories import create_category, get_admin_categories
from JDISCTF.api.admin.challenges import create_challenge, delete_challenge, edit_challenge, \
    get_admin_challenge, get_admin_challenges_for_event
from JDISCTF.api.admin.events import create_event, delete_event, edit_event, get_admin_event, \
    get_admin_events
