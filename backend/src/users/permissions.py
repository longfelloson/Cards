from dataclasses import dataclass

from auth.permissions.core import BasePermission, RolePermission
from auth.permissions.utils import any_permission
from auth.rbac.enums import Role


@dataclass(kw_only=True)
class UsersViewPermissions(BasePermission):
    """Check if a user is an admin"""

    def has_required_permissions(self) -> bool:
        permission = any_permission(
            RolePermission(current_user=self.current_user, required_role=Role.ADMIN)
        )
        return permission
