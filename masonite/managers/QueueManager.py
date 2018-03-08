from masonite.managers.Manager import Manager


class QueueManager(Manager):
    """
    Queue manager class
    """

    config = 'QueueConfig'
    driver_prefix = 'Queue'
