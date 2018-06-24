''' A StatusProvider Service Provider '''
from masonite.provider import ServiceProvider

class ServerErrorExceptionHook:

    def load(self, app):
        if app.make('Application').DEBUG == 'True' or app.make('Application').DEBUG == True:
            return

        request = app.make('Request').status('500 Internal Server Error')
        if app.make('ViewClass').exists('errors/500'):
            rendered_view = app.make('View')('errors/500').rendered_template
        else:
            rendered_view = app.make('View')('/masonite/snippets/statuscode', {'code': '500 Internal Server Error'}).rendered_template

        headers = [
            ("Content-Length", str(len(rendered_view)))
        ]
        app.bind('Headers', headers)
        app.bind('Response', rendered_view)

class StatusCodeProvider(ServiceProvider):

    def register(self):
        self.app.bind('ServiceErrorExceptionHook', ServerErrorExceptionHook())

    def boot(self, StatusCode, Request):
        if StatusCode == '200 OK':
            return

        if StatusCode in ('500 Internal Server Error', '404 Not Found'):
            if self.app.make('ViewClass').exists('errors/{}'.format(StatusCode.split(' ')[0])):
                rendered_view = self.app.make('View')('errors/{}'.format(StatusCode.split(' ')[0])).rendered_template
            else:
                rendered_view = self.app.make('View')('/masonite/snippets/statuscode', {
                    'code': StatusCode
                }).rendered_template
            Headers = [
                ("Content-Length", str(len(rendered_view)))
            ]
            self.app.bind('Response', rendered_view)

            self.app.bind('Headers', Headers)
