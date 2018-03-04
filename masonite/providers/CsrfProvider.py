""" A Csrf Service Provider """
from masonite.provider import ServiceProvider
from masonite.auth.Csrf import Csrf


class CsrfProvider(ServiceProvider):

    wsgi = True

    def register(self):
        request = self.app.make('Request')
        self.app.bind('Request', request)
        self.app.bind('CSRF', Csrf(request))

    def boot(self, View, ViewClass, Request):
        # Share token csrf
        token = Request.get_cookie('csrftoken')

        ViewClass.share({'csrf_field': "<input type='hidden' name='csrf_token' value='{0}' />".format(token)})
