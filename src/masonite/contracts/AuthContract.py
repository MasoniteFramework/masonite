from abc import ABC as Contract, abstractmethod


class AuthContract(Contract):

    @abstractmethod
    def user(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass
