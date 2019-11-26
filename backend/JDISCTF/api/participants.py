from JDISCTF.app import REGISTRY
from JDISCTF.flask_login_authenticator import FlaskLoginAuthenticator
from JDISCTF.models import Participant
from JDISCTF.permission_wrappers import require_participant
from JDISCTF.schemas import ParticipantSchema


@REGISTRY.handles(
    rule="/participant",
    method="GET",
    response_body_schema=ParticipantSchema(),
    authenticators=FlaskLoginAuthenticator()
)
@require_participant
def get_connected_participant(current_participant: Participant):
    """Get the connected participant."""
    return current_participant
