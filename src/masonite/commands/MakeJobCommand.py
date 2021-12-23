"""New Key Command."""
import inflection
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir
from ..utils.location import jobs_path
from .Command import Command


class MakeJobCommand(Command):
    """
    Creates a new job class.

    job
        {name : Name of the job}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        content = render_stub_file(self.get_jobs_path(), name)

        filename = f"{name}.py"
        filepath = jobs_path(filename)
        make_directory(filepath)
        if os.path.exists(filepath) and not self.option("force"):
            self.warning(
                f"{filepath} already exists! Run the command with -f (force) to override."
            )
            return -1
        with open(filepath, "w") as f:
            f.write(content)
        self.info(f"Job Created ({jobs_path(filename, absolute=False)})")

    def get_template_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/templates/")

    def get_jobs_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/jobs/Job.py")
