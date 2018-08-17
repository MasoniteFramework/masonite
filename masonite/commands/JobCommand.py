import os

from cleo import Command

from masonite.app import App
from masonite.helpers.filesystem import make_directory
from masonite.view import View


class JobCommand(Command):
    """
    Creates a new Job

    job
        {name : Name of the job you want to create}
    """

    def handle(self):
        job = self.argument('name')
        view = View(App())
        job_directory = 'app/jobs/{0}.py'.format(job)


        if not make_directory(job_directory):
            return self.error('Job Already Exists!')
        

        f = open(job_directory, 'w+')
        if view.exists('/masonite/snippets/scaffold/job'):
            f.write(
                view.render('/masonite/snippets/scaffold/job',
                            {'class': job.split('/')[-1]}).rendered_template
            )
            self.info('Job Created Successfully!')
            return f.close()
