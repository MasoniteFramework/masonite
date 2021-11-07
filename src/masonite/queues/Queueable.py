"""Base Queue Module."""


class Queueable:
    """Makes classes Queueable."""

    run_again_on_fail = True
    run_times = 3

    def handle(self):
        pass

    def failed(self, obj, e):
        pass

    def __repr__(self):
        return self.__class__.__name__
