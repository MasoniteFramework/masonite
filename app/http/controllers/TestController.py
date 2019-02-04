from cleo import Command
from masonite.exceptions import DebugException

from masonite.request import Request


class TestController:

    def __init__(self):
        self.test = True

    def show(self):
        pass

    def change_header(self, request: Request):
        request.header('Content-Type', 'application/xml')
        return 'test'

    def change_status(self, request: Request):
        request.status(203)
        return 'test'

    def testing(self):
        return 'test'

    def json_response(self):
        return {'id': 1}

    def post_test(self):
        return 'post_test'

    def json(self):
        return 'success'

    def session(self, request: Request):
        request.session.set('test', 'value')
        return 'session set'
