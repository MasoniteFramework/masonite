from abc import ABC as Contract, abstractmethod

class AuthManagerContract(Contract):

    def user(self):
        pass
    
    def save(self):
        pass

