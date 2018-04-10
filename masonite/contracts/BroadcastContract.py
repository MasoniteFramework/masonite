from abc import ABC, abstractmethod


class BroadcastContract(ABC):

    @abstractmethod
    def ssl(self): pass

    @abstractmethod
    def channel(self): pass
