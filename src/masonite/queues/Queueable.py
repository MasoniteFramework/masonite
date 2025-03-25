"""Base Queue Module."""


class Queueable:
    """Makes classes Queueable."""

    run_again_on_fail = True
    run_times = 3

    def queue(self):
        return "default"

    def handle(self):
        pass

    def failed(self, obj, e):
        pass

    def __repr__(self):
        return self.__class__.__name__

    def send(self, notification, driver="", dry=False, fail_silently=False):
        from ..facades.Queue import Queue
        Queue.push(notification, queue=self.queue())
        print('Sending to queue', notification)
