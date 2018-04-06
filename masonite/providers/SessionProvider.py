""" A RedirectionProvider Service Provider """
from masonite.provider import ServiceProvider
from masonite.session import Session


class SessionProvider(ServiceProvider):

    def register(self):
        pass

    def boot(self, Environ, Request, ViewClass):
        session = Session(Environ)
        
        self.app.bind('Session', session)
        Request.session = session

        ViewClass.share({
            'session': session.helper
        })
        
