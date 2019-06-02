from abc import ABC as Contract, abstractmethod


class AuthManagerContract(Contract):

    @abstractmethod
    def user(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass
