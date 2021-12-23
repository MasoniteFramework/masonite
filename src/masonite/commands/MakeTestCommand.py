"""New Test Command."""
import inflection
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir
from .Command import Command


class MakeTestCommand(Command):
    """
    Creates a new test class.

    test
        {name : Name of the test case (CamelCase) }
        {--d|--directory=tests/unit : Directory to create the test file}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        test_filename = f"test_{inflection.underscore(self.argument('name').replace('Test', '').replace('test', ''))}.py"
        directory = self.option("directory")
        content = render_stub_file(self.get_testcase_path(), name)

        filepath = os.path.join(directory, test_filename)
        make_directory(filepath)
        if os.path.exists(filepath) and not self.option("force"):
            self.warning(
                f"{filepath} already exists! Run the command with -f (force) to override."
            )
            return -1
        with open(filepath, "w") as f:
            f.write(content)
        self.info(f"Test Created ({filepath})")

    def get_testcase_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/tests/TestCase.py")
