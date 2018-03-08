class Queueable:

    def handle(self):
        pass

    def dispatch(self):
        return self.handle
