"""Auth Manager Module."""

from masonite.managers import Manager


class AuthManager(Manager):
    """Manages all auth drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'AuthConfig'
    driver_prefix = 'Auth'


class Auth:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
