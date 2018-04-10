from masonite.managers.Manager import Manager


class SessionManager(Manager):
    """
    Session manager class
    """

    config = 'SessionConfig'
    driver_prefix = 'Session'
