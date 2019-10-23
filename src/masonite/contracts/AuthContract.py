from abc import ABC as Contract, abstractmethod

from masonite.interfaces import Interface

class AuthInterface(Interface):

    def user(self, auth_model):
        pass

    def save(self, remember_token, **options):
        pass

    def delete(self):
        pass

class AuthContract(AuthInterface):
    pass
    # @abstractmethod
    # def user(self):
    #     pass

    # @abstractmethod
    # def save(self):
    #     pass

    # @abstractmethod
    # def delete(self):
    #     pass
