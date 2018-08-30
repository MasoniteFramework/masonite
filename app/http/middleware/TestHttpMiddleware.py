class TestHttpMiddleware:
    ''' Test Middleware '''

    def __init__(self, Request):
        ''' Inject Any Dependencies From The Service Container '''
        self.request = Request

    def before(self):
        ''' Run This Middleware Before The Route Executes '''
        self.request.environ['HTTP_TEST'] = 'test'
