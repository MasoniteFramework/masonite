"""Session Manager Module."""

from masonite.contracts import SessionManagerContract
from masonite.managers import Manager


class SessionManager(Manager, SessionManagerContract):
    """Manages all session drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'SessionConfig'
    driver_prefix = 'Session'


class Session:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
