from fastapi import Request

from auth.rbac.enforce import ENFORCER
from config import settings


def has_access_to_resource(request: Request) -> bool:
    resource = get_request_resource(request.url.path)
    action = request.method.casefold()
    
    if ENFORCER.enforce(request.user.role, resource, action):
        return True
    return False


def get_request_resource(request_path: str) -> str:
    """Extract the resource path

    Args:
        path (str): path of request

    Returns:
        str: "/api/users/123" → "users" or "users/:id
    """
    request_resource = request_path.replace(f"{settings.api_prefix}/", "").strip()
    return request_resource
