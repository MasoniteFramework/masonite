"""New Rule Command."""
from cleo import Command
import inflection
import os

from ...utils.filesystem import get_module_dir, make_directory, render_stub_file
from ...utils.location import base_path
from ...utils.str import as_filepath


class MakeRuleCommand(Command):
    """
    Creates a new rule.

    rule
        {name : Name of the rule}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        content = render_stub_file(self.get_stub_rule_path(), name)

        relative_filename = os.path.join(
            as_filepath(self.app.make("validation.location")), name + ".py"
        )

        if os.path.exists(relative_filename):
            return self.line(
                f"<error>File ({relative_filename}) already exists</error>"
            )

        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)

        self.info(f"Validation Rule Created ({relative_filename})")

    def get_stub_rule_path(self):
        return os.path.join(get_module_dir(__file__), "../../stubs/validation/Rule.py")
