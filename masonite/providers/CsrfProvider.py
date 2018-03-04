""" A Csrf Service Provider """
from masonite.provider import ServiceProvider
from masonite.auth.Csrf import Csrf


class CsrfProvider(ServiceProvider):

    wsgi = True

    def register(self):
        self.app.bind('CSRF', Csrf(self.app.make('Request')))

    def boot(self, View, ViewClass, Request):
        # Share token csrf
        token = Request.get_cookie('csrftoken')

        ViewClass.share({'csrf_field': "<input type='hidden' name='csrf_token' value='{0}' />".format(token)})
