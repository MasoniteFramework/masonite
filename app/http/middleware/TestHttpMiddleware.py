from masonite.request import Request

class TestHttpMiddleware:
    ''' Test Middleware '''

    def __init__(self, request: Request):
        ''' Inject Any Dependencies From The Service Container '''
        self.request = request

    def before(self):
        ''' Run This Middleware Before The Route Executes '''
        self.request.environ['HTTP_TEST'] = 'test'
