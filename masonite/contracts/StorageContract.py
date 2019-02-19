from abc import ABC as Contract
from abc import abstractmethod


class StorageContract(Contract):

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def append(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def exists(self):
        pass

    @abstractmethod
    def driver(self):
        pass

    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def extension(self):
        pass

    @abstractmethod
    def upload(self):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def make_directory(self):
        pass

    @abstractmethod
    def delete_directory(self):
        pass

    @abstractmethod
    def move(self):
        pass
