class Pipeline:
    def __init__(self, payload, *args):
        self.payload = payload
        self.args = args

    def through(self, pipe_list, handler="handle"):
        passthrough = self.payload
        for pipe in pipe_list:
            response = getattr(pipe(), handler)(self.payload, *self.args)
            if response != passthrough:
                return False

        return True
