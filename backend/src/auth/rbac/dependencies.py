from fastapi import Depends, Request

from auth.dependencies import get_current_user
from auth.rbac.exceptions import AccessDeniedException
from auth.rbac.utils import get_request_resource, has_access_to_resource
from users.models import User


async def check_permissions(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    user_id = request.path_params.get("user_id")

    if user_id:
        if user_id != str(current_user.id):
            raise AccessDeniedException()

    resource = get_request_resource(request.url.path)
    action = request.method.casefold()

    if not has_access_to_resource(current_user, resource, action):
        raise AccessDeniedException()
