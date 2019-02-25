"""A StatusProvider Service Provider."""

from config import application
from masonite.response import Response
from masonite.provider import ServiceProvider


class ServerErrorExceptionHook:

    def load(self, app):
        if application.DEBUG:
            return

        request = app.make('Request')

        request.status(500)
        if app.make('ViewClass').exists('errors/500'):
            rendered_view = app.make('View')('errors/500')
        else:
            rendered_view = app.make('View')(
                '/masonite/snippets/statuscode', {'code': '500 Internal Server Error'})

        request.app().make(Response).view(rendered_view)


class StatusCodeProvider(ServiceProvider):

    def register(self):
        self.app.bind('ServiceErrorExceptionHook', ServerErrorExceptionHook())

    def boot(self):
        request = self.app.make('Request')
        response = self.app.make(Response)
        if request.is_status(200):
            return

        if request.get_status() in (500, 405, 404):
            if self.app.make('ViewClass').exists('errors/{}'.format(request.get_status())):
                rendered_view = self.app.make('View')(
                    'errors/{}'.format(request.get_status()))
            else:
                rendered_view = self.app.make('View')('/masonite/snippets/statuscode', {
                    'code': request.get_status_code()
                })

            response.view(rendered_view, status=request.get_status())
