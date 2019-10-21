"""A RedirectionProvider Service Provider."""

from ..drivers import SessionCookieDriver, SessionMemoryDriver
from ..managers import SessionManager
from ..provider import ServiceProvider
from ..view import View
from ..request import Request
from .. import Session
from ..helpers import config


class SessionProvider(ServiceProvider):

    def register(self):
        # from config import session
        # self.app.bind('SessionConfig', session)
        self.app.bind('SessionMemoryDriver', SessionMemoryDriver)
        self.app.bind('SessionCookieDriver', SessionCookieDriver)
        self.app.bind('SessionManager', SessionManager(self.app))

    def boot(self, request: Request, view: View, session: SessionManager):
        self.app.bind('Session', session.driver(config('session').DRIVER))
        self.app.swap(Session, session.driver(config('session').DRIVER))
        request.session = self.app.make('Session')

        view.share({
            'session': self.app.make('Session').helper
        })
