"""New Rule Enclosure Command."""
import inflection
import os

from ...utils.filesystem import get_module_dir, make_directory, render_stub_file
from ...utils.location import base_path
from ...utils.str import as_filepath
from ...commands.Command import Command


class MakeRuleEnclosureCommand(Command):
    """
    Creates a new rule enclosure.

    rule:enclosure
        {name : Name of the rule enclosure}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        content = render_stub_file(self.get_stub_rule_enclosure_path(), name)

        relative_filename = os.path.join(
            as_filepath(self.app.make("validation.location")), name + ".py"
        )

        if os.path.exists(relative_filename) and not self.option("force"):
            self.warning(
                f"{relative_filename} already exists! Run the command with -f (force) to override."
            )
            return -1

        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)

        self.info(f"Validation Created ({relative_filename})")

    def get_stub_rule_enclosure_path(self):
        return os.path.join(
            get_module_dir(__file__), "../../stubs/validation/RuleEnclosure.py"
        )
