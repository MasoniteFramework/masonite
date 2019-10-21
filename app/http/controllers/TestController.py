from app.jobs.TestJob import TestJob
from src.masonite import Queue, Mail
from src.masonite.request import Request

class TestController:

    def __init__(self):
        self.test = True

    def show(self):
        return 'show'

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
        return {'id': 1}

    def post_test(self):
        return 'post_test'

    def json(self):
        return 'success'

    def bad(self):
        return 5 / 0

    def session(self, request: Request):
        request.session.set('test', 'value')
        return 'session set'

    def queue(self, queue: Queue):
        # queue.driver('amqp').push(self.bad)
        queue.driver('amqp').push(TestJob, channel='default')
        return 'queued'

    def mail(self, mail: Mail):
        return mail.to('idmann509@gmail.com').template('test', {'test': 'mail'})
