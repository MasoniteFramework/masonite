''' A User Model Service Provider '''
from masonite.provider import ServiceProvider
from app.User import User

class UserModelProvider(ServiceProvider):
    ''' Binds the User model into the Service Container '''

    wsgi = False

    def register(self):
        ''' Registers The User Into The Service Container '''
        self.app.bind('User', User)

    def boot(self):
        pass
