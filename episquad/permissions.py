from enum import Enum

class Permissions(Enum):
    ADMIN = 'admin'
    DAY = 'day'
    ADD_USER = 'add-user'
    REM_USER = 'remove-user'
    ADD_PERMS = 'add-perms'
    REM_PERMS = 'rem-perms'
    ADD_GROUPS = 'add-groups'
    REM_GROUPS = 'rem-groups'

def exists(perm):
    for p in Permissions:
        if p.value == perm:
            return True
    return False

def exists_multiple(perms):
    for perm in perms:
        if not exists(perm):
            return False
    return True 

def has_permissions(user, perms):
    return all(p.value in user['permissions'] for p in perms) or Permissions.ADMIN.value in user['permissions']
