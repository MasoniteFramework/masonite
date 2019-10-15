from masonite.request import Request
from .BaseExceptionListener import BaseExceptionListener

class ExceptionListener(BaseExceptionListener):

    listens = [
        ZeroDivisionError
    ]

    def __init__(self, request: Request):
        self.request = request

    def handle(self, exception):
        self.request.error_thrown = True