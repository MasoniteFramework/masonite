import os
from cleo import Command


class JobCommand(Command):
    """
    Creates a new Job

    job
        {name : Name of the job you want to create}
    """

    def handle(self):
        job = self.argument('name')
        if not os.path.isfile('app/jobs/{0}.py'.format(job)):
            if not os.path.exists(os.path.dirname('app/jobs/{0}.py'.format(job))):
                # Create the path to the job if it does not exist
                os.makedirs(os.path.dirname('app/jobs/{0}.py'.format(job)))

            f = open('app/jobs/{0}.py'.format(job), 'w+')

            f.write("''' A {0} Queue Job '''\n\n".format(job))
            f.write('from masonite.queues.Queueable import Queueable\n\n')
            f.write("class {0}(Queueable):\n\n    ".format(job))
            f.write("def __init__(self):\n        pass\n\n    ")
            f.write("def handle(self):\n        pass\n")

            self.info('Job Created Successfully!')
        else:
            self.comment('Job Already Exists!')
