"""Creates New Test Command."""
from masonite.commands import BaseScaffoldCommand


class TestCommand(BaseScaffoldCommand):
    """
    Creates a new test case.

    test
        {name : Name of the test you would like to create}
    """

    scaffold_name = 'Test'
    postfix = ""
    prefix = "Test"
    template = '/masonite/snippets/scaffold/test'
    base_directory = 'tests/test_'
    file_to_lower = True
