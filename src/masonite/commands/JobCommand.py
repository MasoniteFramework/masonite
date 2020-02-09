"""New Job Command."""
from ..commands import BaseScaffoldCommand


class JobCommand(BaseScaffoldCommand):
    """
    Creates a new Job.

    job
        {name : Name of the job you want to create}
    """

    scaffold_name = 'Job'
    template = '/masonite/snippets/scaffold/job'
    base_directory = 'app/jobs/'
    postfix = "Job"
