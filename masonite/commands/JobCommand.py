""" New Job Command """
from cleo import Command


class JobCommand(Command):
    """
    Creates a new Job

    job
        {name : Name of the job you want to create}
    """

    scaffold_name = 'Job'
    template = '/masonite/snippets/scaffold/job'
    base_directory = 'app/jobs/'
