""" A TestJob Queue Job """

from masonite.queues import Queueable


class TestJob(Queueable):
    """A TestJob Job
    """

    def __init__(self):
        """A TestJob Constructor
        """

        pass

    def handle(self):
        """Logic to handle the job
        """

        return 2/0
    
    def failed(self, payload, error):
        print('running a failed job hook')