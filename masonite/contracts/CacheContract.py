from abc import ABC, abstractmethod


class CacheContract(ABC):

    @abstractmethod
    def store(self): pass

    @abstractmethod
    def store_for(self): pass

    @abstractmethod
    def get(self): pass

    @abstractmethod
    def is_valid(self): pass

    @abstractmethod
    def cache_exists(self): pass
