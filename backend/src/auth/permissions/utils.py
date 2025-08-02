from auth.permissions.exceptions import NotEnoughPermissionsException


def all_permissions(*permissions) -> bool:
    for permission in permissions:
        try:
            permission().check_permissions()
        except NotEnoughPermissionsException:
            return False

    return True


def any_permission(*permissions) -> bool:
    for permission in permissions:
        try:
            permission.check_permissions()
            return True
        except NotEnoughPermissionsException:
            pass
    return False
