
class BaseDriver:
    """Base Session driver"""

    def __init__(self, application: "Application"):
        self.application = application
        self.driver_config = {}
        self.options = {}

    def set_options(self, options):
        # allow internal driver defaults
        if options:
            self.driver_config.update(options.pop("driver_config", {}))
            self.options = options
        return self
