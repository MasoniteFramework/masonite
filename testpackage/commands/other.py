from cleo import Command


class OtherPackageCommand(Command):
    """
    Test Commands for unit tests only.

    testother
    """

    def handle(self):
        print("test package command")
