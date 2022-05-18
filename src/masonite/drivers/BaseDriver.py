
class BaseDriver:
    """Base Session driver"""

    def __init__(self, application: "Application"):
        self.application = application
        self.options = {}

    def set_options(self, options):
        # allow internal driver defaults
        self.options.update(options)
        return self
