""" Controller module """


class Controller:
    """
    Base Class for Controllers
    """

    def __init__(self):
        self.app = None

    def load_app(self, app):
        """ Loads the container into the controller """
        self.app = app
        return self
