class HasColoredOutput:
    """Add level-colored output print functions to a class."""

    def success(self, message: str):
        print("\033[92m {0} \033[0m".format(message))

    def warning(self, message: str):
        print("\033[93m {0} \033[0m".format(message))

    def danger(self, message: str):
        print("\033[91m {0} \033[0m".format(message))

    def info(self, message: str):
        return self.success(message)


class AddCommandColors:
    """The default style set used by Cleo is defined here:
    https://github.com/sdispater/clikit/blob/master/src/clikit/formatter/default_style_set.py
    This mixin add method helper to output errors and warnings.
    """

    def error(self, text: str):
        """Write a string with error output style."""
        self.line(text, "error")

    def warning(self, text: str):
        """Write a string with warning output style."""
        self.line(text, "c2")
