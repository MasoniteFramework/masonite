class PusherDriver:
    def __init__(self, application):
        self.application = application
        self.connection = None

    def set_options(self, options):
        self.options = options
        return self

    def get_connection(self):
        try:
            import pusher
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'pusher' library. Run 'pip install pusher' to fix this."
            )

        if self.connection:
            return self.connection

        self.connection = pusher.Pusher(
            app_id=str(self.options.get("app_id")),
            key=self.options.get("client"),
            secret=self.options.get("secret"),
            cluster=self.options.get("cluster"),
            ssl=self.options.get("ssl"),
        )

        return self.connection

    def channel(self, channel, event, value):
        return self.get_connection().trigger(channel, event, value)

    def authorize(self, channel, socket_id):
        return self.get_connection().authenticate(channel=channel, socket_id=socket_id)
