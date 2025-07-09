from auth.rbac.enforce import ENFORCER
from auth.rbac.enums import Action, Resource
from users.models import User


def has_access_to_resource(user: User, resource: Resource, action: Action) -> bool:
    if ENFORCER.enforce(user.role, resource, action):
        return True
    return False


def get_request_resource(request_path: str) -> str:
    """Extract the resource path in the format: /<first>/<second>

    Args:
        path (str): path of request

    Returns:
        str: "/api/users/123" → "/api/users"
    """
    parts = request_path.strip("/").split("/")
    if len(parts) >= 2:
        return f"/{parts[0]}/{parts[1]}"
    return request_path
