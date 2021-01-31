from cleo import Command


class TestPackageDemoCommand(Command):
    """
    Test Commands for unit tests only.

    testdemo
    """

    def handle(self):
        print("test package command")
