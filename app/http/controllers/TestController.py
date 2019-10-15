from app.jobs.TestJob import TestJob
from masonite import Queue
from masonite.request import Request
from masonite.view import View

class TestController:

    def __init__(self):
        self.test = True

    def show(self):
        return 'show'

    def v(self, view: View):
        return view.render('test')

    def change_header(self, request: Request):
        request.header('Content-Type', 'application/xml')
        return 'test'

    def change_status(self, request: Request):
        request.status(203)
        return 'test'

    def change_404(self, request: Request):
        request.status(404)
        return 'test'

    def testing(self):
        return 'test'

    def json_response(self, request: Request):
        return {'id': 2}

    def post_test(self):
        return 'post_test'

    def json(self):
        return 'success'

    def bad(self):
        return 5 / 0

    def keyerror(self):
        x = {'hello': 'world'}
        return x['test']

    def session(self, request: Request):
        request.session.set('test', 'value')
        return 'session set'

    def queue(self, queue: Queue):
        # queue.driver('amqp').push(self.bad)
        queue.driver('amqp').push(TestJob, channel='default')
        return 'queued'
