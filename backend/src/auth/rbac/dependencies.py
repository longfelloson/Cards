from fastapi import Request, Depends
from auth.dependencies import get_current_user
from users.models import User, Role
from auth.rbac.exceptions import AccessDeniedException
from auth.rbac.utils import has_access_to_resource, get_request_resource

USER_ID_KEY = "user_id"


async def check_permissions(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    if current_user.role == Role.ADMIN:
        return

    current_user_id = str(current_user.id)
    path_user_id = request.path_params.get(USER_ID_KEY)
    query_user_id = request.query_params.get(USER_ID_KEY)

    if not (path_user_id == current_user_id or query_user_id == current_user_id):
        raise AccessDeniedException()

    resource = get_request_resource(request.url.path)
    action = request.method.casefold()

    if not has_access_to_resource(current_user, resource, action):
        raise AccessDeniedException()
