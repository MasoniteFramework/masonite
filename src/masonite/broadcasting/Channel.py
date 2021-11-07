class Channel:
    def __init__(self, name):
        self.name = name

    def authorized(self, application):
        return True
