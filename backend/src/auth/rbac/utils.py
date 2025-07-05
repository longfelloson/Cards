from auth.rbac.enums import Action, Resource
from auth.rbac.enforce import ENFORCER
from users.models import User


def has_access_to_resource(user: User, resource: Resource, action: Action) -> bool:
    if ENFORCER.enforce(user.role, resource, action):
        return True
    return False
