from abc import ABC, abstractmethod


class BroadcastContract(ABC):

    @abstractmethod
    def store(self): pass
