from dataclasses import dataclass

NOT_ENOUGH_PERMISSIONS_DETAIL = "User doesn't have enough permissions to view endpoint"


@dataclass
class NotEnoughPermissionsException(Exception):
    permission: object
    