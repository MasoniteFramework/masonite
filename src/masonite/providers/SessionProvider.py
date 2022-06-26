from .Provider import Provider
from ..sessions import Session
from ..drivers.session import CookieDriver, RedisDriver
from ..configuration import config
from ..sessions import old


class SessionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        session = Session(self.application).set_configuration(config("session.drivers"))
        session.add_driver("cookie", CookieDriver(self.application))
        session.add_driver("redis", RedisDriver(self.application))
        self.application.bind("session", session)
        self.application.make("view").share({"old": old})

    def boot(self):
        pass
