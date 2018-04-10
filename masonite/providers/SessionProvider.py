""" A RedirectionProvider Service Provider """
from config import session
from masonite.drivers.SessionMemoryDriver import SessionMemoryDriver
from masonite.drivers.SessionCookieDriver import SessionCookieDriver
from masonite.managers.SessionManager import SessionManager
from masonite.provider import ServiceProvider


class SessionProvider(ServiceProvider):

    def register(self):
        self.app.bind('SessionConfig', session)
        self.app.bind('SessionMemoryDriver', SessionMemoryDriver)
        self.app.bind('SessionCookieDriver', SessionCookieDriver)
        self.app.bind('SessionManager', SessionManager(self.app))

    def boot(self, Environ, Request, ViewClass, SessionManager, SessionConfig):
        self.app.bind('Session', SessionManager.driver(SessionConfig.DRIVER))
        Session = self.app.make('Session')
        Request.session = Session

        ViewClass.share({
            'session': Session.helper
        })
