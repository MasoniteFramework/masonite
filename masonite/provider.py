class ServiceProvider():

    wsgi = True

    def __init__(self):
        self.app = None

    def boot(self):
        pass

    def register(self):
        self.app.bind('Request', object)

    def load_app(self, app):
        self.app = app
        return self
