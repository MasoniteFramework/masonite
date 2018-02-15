class Queueable(object):

    def handle(self):
        pass

    def dispatch(self):
        return self.handle

