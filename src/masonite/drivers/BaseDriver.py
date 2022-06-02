from mergedeep import merge

class BaseDriver:
    """Base Session driver"""

    def __init__(self, application: "Application"):
        self.application = application
        self.default_options = {}
        self.options = {}

    def set_options(self, options: dict):
        # merge options with defaults
        self.options = merge(self.default_options, self.options, options)
        return self
