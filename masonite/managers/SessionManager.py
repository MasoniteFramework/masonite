""" Session Manager Module """

from masonite.managers.Manager import Manager


class SessionManager(Manager):
    """Manages all session drivers.

    Arguments:
        Manager {masonite.managers.Manager} -- The base Manager class.
    """

    config = 'SessionConfig'
    driver_prefix = 'Session'
