class Hook:

    def __init__(self, app):
        self._app = app

    def fire(self, search):
        for key in self._app.collect(search):
            self._app.make(key).load(self._app)
