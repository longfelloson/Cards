from fastapi import Request
from auth.rbac.utils import has_access_to_resource
from auth.rbac.exceptions import ResourceNotFound


class AccessDependency:
    async def __call__(self, request: Request):
        if not has_access_to_resource(request):
            raise ResourceNotFound()
            