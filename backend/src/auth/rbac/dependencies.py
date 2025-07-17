from fastapi import Request

from auth.rbac.enums import Role
from auth.rbac.exceptions import ResourceNotFound
from auth.rbac.utils import has_access_to_resource


class RoleAccessDependency:
    async def __call__(self, request: Request):
        if request.user.role == Role.ADMIN:
            return

        if not has_access_to_resource(request, request.user):
            raise ResourceNotFound()
