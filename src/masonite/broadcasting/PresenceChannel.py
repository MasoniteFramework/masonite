class PresenceChannel:
    def __init__(self, name):
        if not name.startswith("presence-"):
            name = "presence-" + name

        self.name = name

    def authorized(self, application):
        return bool(application.make("request").user())
