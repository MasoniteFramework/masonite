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


class AddCommandColors:
    """The default style set used by Cleo is defined here:
    https://github.com/sdispater/clikit/blob/master/src/clikit/formatter/default_style_set.py
    This mixin add method helper to output errors and warnings.
    """

    def error(self, text):
        """
        Write a string as information output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, "error")

    def warning(self, text):
        """
        Write a string as information output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, "c2")
