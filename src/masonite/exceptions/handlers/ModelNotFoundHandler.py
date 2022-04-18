from ..exceptions import ModelNotFoundException


class ModelNotFoundHandler:
    def __init__(self, application):
        self.application = application

    def handle(self, exception):
        masonite_exception = ModelNotFoundException()
        self.application.make("exception_handler").handle(masonite_exception)
