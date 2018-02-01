from masonite.provider import ServiceProvider
from app.User import User

class UserModelProvider(ServiceProvider):
    ''' Binds the User model into the Service Container '''

    def register(self):
        self.app.bind('User', User)

    def boot(self):
        pass
