from JDISCTF.app import REGISTRY
from JDISCTF.models import Administrator
from JDISCTF.permission_wrappers import require_admin
from JDISCTF.schemas import AdministratorSchema


@REGISTRY.handles(
    rule="/admin/admin",
    method="GET",
    response_body_schema=AdministratorSchema()
)
@require_admin
def get_connected_admin(current_admin: Administrator):
    """Get the connected admin."""
    return current_admin
