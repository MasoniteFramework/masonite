from cleo import Command

from masonite.request import Request

class TestController:

    def __init__(self):
        self.test = True

    def show(self):
        pass
    
    def testing(self):
        return 'test'
    
    def post_test(self):
        return 'post_test'

    def json(self):
        return 'success'

    def session(self, request: Request):
        request.session.set('test', 'value')
        return 'session set'
