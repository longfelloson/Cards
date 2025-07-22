from fastapi import Request

from auth.permissions import BasePermission


class UserOwnerPermission(BasePermission):
    async def has_required_permissions(self, request: Request) -> bool:
        """
        Check if user requests his own resource
        """
        user_id = request.path_params['user_id']
        return str(request.user.id) == user_id
