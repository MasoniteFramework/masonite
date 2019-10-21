"""Session Manager Module."""

from ..contracts import SessionManagerContract
from .Manager import Manager


class SessionManager(Manager, SessionManagerContract):
    """Manages all session drivers.

    Arguments:
        Manager {from .managers.Manager} -- The base Manager class.
    """

    config = 'session'
    driver_prefix = 'Session'


class Session:
    """Dummy class that will be used to swap out the manager in the container."""

    pass
