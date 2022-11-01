class Pipeline:
    """Masonite Pipeline class allowing to run sequentially a list of classes with a handler
    method until it fails."""

    def __init__(self, payload, *args):
        self.payload = payload
        self.args = args

    def through(self, pipe_list: list, handler: str = "handle") -> bool:
        """Run the given handler of each element in the pipeline. Payload and additional
        arguments will be passed to the handler method."""
        passthrough = self.payload
        for pipe in pipe_list:
            response = getattr(pipe(), handler)(self.payload, *self.args)
            if response != passthrough:
                return False

        return True
