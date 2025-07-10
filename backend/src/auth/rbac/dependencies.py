from auth.dependencies import get_current_user
from auth.rbac.exceptions import AccessDeniedException
from auth.rbac.utils import get_request_resource, has_access_to_resource
from fastapi import Depends, Request
from users.models import User

USER_ID_KEY = "user_id"


async def check_permissions(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    path_user_id = request.path_params.get(USER_ID_KEY)
    query_user_id = request.query_params.get(USER_ID_KEY)
    
    if path_user_id and path_user_id != str(current_user.id):
        raise AccessDeniedException()
    
    if query_user_id and query_user_id != str(current_user.id):
        raise AccessDeniedException()
    
    resource = get_request_resource(request.url.path)
    action = request.method.casefold()

    if not has_access_to_resource(current_user, resource, action):
        raise AccessDeniedException()
