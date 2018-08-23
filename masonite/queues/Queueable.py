""" Base Queue Module """

class Queueable:
    """Makes classes Queueable.
    """

    def handle(self):
        """Put the queue logic in this handle method
        """

        pass

    def dispatch(self):
        """Responsible for dispatching the job to the Queue service
        
        Returns:
            self.handle
        """
        
        return self.handle
