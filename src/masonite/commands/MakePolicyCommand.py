"""New Policy Command."""
import inflection
import os
from cleo import Command

from ..utils.filesystem import make_directory


class MakePolicyCommand(Command):
    """
    Creates a new policy class.

    policy
        {name : Name of the policy}
        {--model=? : Create a policy for a model with a set of predefined methods}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        if not name.endswith("Policy"):
            name += "Policy"

        if self.option("model"):
            with open(self.get_model_policy_path(), "r") as f:
                content = f.read()
                content = content.replace("__class__", name)
        else:
            with open(self.get_base_policy_path(), "r") as f:
                content = f.read()
                content = content.replace("__class__", name)

        file_name = os.path.join(
            self.app.make("policies.location").replace(".", "/"), name + ".py"
        )

        make_directory(file_name)

        with open(file_name, "w") as f:
            f.write(content)
        self.info(f"Policy Created ({file_name})")

    def get_template_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/templates/")

    def get_base_policy_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(current_path, "../stubs/policies/Policy.py")

    def get_model_policy_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(current_path, "../stubs/policies/ModelPolicy.py")
