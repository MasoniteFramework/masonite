"""A StatusProvider Service Provider."""

from config import application
from masonite.provider import ServiceProvider


class ServerErrorExceptionHook:

    def load(self, app):
        if application.DEBUG:
            return

        request = app.make('Request')

        request.status(500)
        if app.make('ViewClass').exists('errors/500'):
            rendered_view = app.make('View')('errors/500').rendered_template
        else:
            rendered_view = app.make('View')(
                '/masonite/snippets/statuscode', {'code': '500 Internal Server Error'}).rendered_template

        request.header('Content-Length', str(len(rendered_view)))
        app.bind('Response', rendered_view)


class StatusCodeProvider(ServiceProvider):

    def register(self):
        self.app.bind('ServiceErrorExceptionHook', ServerErrorExceptionHook())

    def boot(self):
        request = self.app.make('Request')
        if request.get_status_code() == '200 OK':
            return

        if request.get_status_code() in ('500 Internal Server Error', '404 Not Found', '503 Service Unavailable'):
            if self.app.make('ViewClass').exists('errors/{}'.format(request.get_status_code().split(' ')[0])):
                rendered_view = self.app.make('View')(
                    'errors/{}'.format(request.get_status_code().split(' ')[0])).rendered_template
            else:
                rendered_view = self.app.make('View')('/masonite/snippets/statuscode', {
                    'code': request.get_status_code()
                }).rendered_template

            self.app.make('Request').header('Content-Length', str(len(rendered_view)))
            self.app.bind('Response', rendered_view)
