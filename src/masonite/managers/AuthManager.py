"""Auth Manager Module."""

from .Manager import Manager


class AuthManager(Manager):
    """Manages all auth drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'auth'
    driver_prefix = 'Auth'


class Auth:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
