from fastapi import Request

from auth.permissions import BasePermission
from auth.rbac.enums import Role
from users.service import users_service


class UserViewPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        if request.user.role == Role.ADMIN:
            return True

        user_id = request.path_params["user_id"]
        user = await users_service.get(user_id=user_id, uow=request.state.uow)

        return user.id == request.user.id
