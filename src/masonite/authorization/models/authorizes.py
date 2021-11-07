from ...facades import Gate


class Authorizes:
    def can(self, permission, *args):
        return Gate.for_user(self).allows(permission, *args)

    def cannot(self, permission, *args):
        return Gate.for_user(self).denies(permission, *args)

    def can_any(self, permissions, *args):
        return Gate.for_user(self).any(permissions, *args)
