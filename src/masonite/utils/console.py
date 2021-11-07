class HasColoredOutput:
    """Add level-colored output print functions to a class."""

    def success(self, message):
        print("\033[92m {0} \033[0m".format(message))

    def warning(self, message):
        print("\033[93m {0} \033[0m".format(message))

    def danger(self, message):
        print("\033[91m {0} \033[0m".format(message))

    def info(self, message):
        return self.success(message)
