from ..facades import Gate


class AuthorizesRequest:
    """Request mixin to add permission handling to requests."""

    def authorize(self, permission: str, *args):
        """Check if the user performing the current request has the given permission."""
        return Gate.authorize(permission, *args)
