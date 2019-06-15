"""A RedirectionProvider Service Provider."""

from masonite.drivers import SessionCookieDriver, SessionMemoryDriver
from masonite.managers import SessionManager
from masonite.provider import ServiceProvider
from masonite.view import View
from masonite.request import Request
from masonite import Session


class SessionProvider(ServiceProvider):

    def register(self):
        from config import session
        self.app.bind('SessionConfig', session)
        self.app.bind('SessionMemoryDriver', SessionMemoryDriver)
        self.app.bind('SessionCookieDriver', SessionCookieDriver)
        self.app.bind('SessionManager', SessionManager(self.app))

    def boot(self, request: Request, view: View, session: SessionManager):
        self.app.bind('Session', session.driver(self.app.make('SessionConfig').DRIVER))
        self.app.swap(Session, session.driver(self.app.make('SessionConfig').DRIVER))
        request.session = self.app.make('Session')

        view.share({
            'session': self.app.make('Session').helper
        })
