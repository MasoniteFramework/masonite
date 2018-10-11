"""A StatusProvider Service Provider."""

from masonite.provider import ServiceProvider
from config import application


class ServerErrorExceptionHook:

    def load(self, app):
        if application.DEBUG:
            return

        app.make('Request').status(500)
        if app.make('ViewClass').exists('errors/500'):
            rendered_view = app.make('View')('errors/500').rendered_template
        else:
            rendered_view = app.make('View')(
                '/masonite/snippets/statuscode', {'code': '500 Internal Server Error'}).rendered_template

        headers = [
            ("Content-Length", str(len(rendered_view)))
        ]
        app.bind('Headers', headers)
        app.bind('Response', rendered_view)


class StatusCodeProvider(ServiceProvider):

    def register(self):
        self.app.bind('ServiceErrorExceptionHook', ServerErrorExceptionHook())

    def boot(self):
        if self.app.make('StatusCode') == '200 OK':
            return

        if self.app.make('StatusCode') in ('500 Internal Server Error', '404 Not Found', '503 Service Unavailable'):
            if self.app.make('ViewClass').exists('errors/{}'.format(self.app.make('StatusCode').split(' ')[0])):
                rendered_view = self.app.make('View')(
                    'errors/{}'.format(self.app.make('StatusCode').split(' ')[0])).rendered_template
            else:
                rendered_view = self.app.make('View')('/masonite/snippets/statuscode', {
                    'code': self.app.make('StatusCode')
                }).rendered_template
            Headers = [
                ("Content-Length", str(len(rendered_view)))
            ]
            self.app.bind('Response', rendered_view)

            self.app.bind('Headers', Headers)
