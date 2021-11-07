from ..facades import Gate


class AuthorizesRequest:
    def authorize(self, permission, *args):

        return Gate.authorize(permission, *args)
