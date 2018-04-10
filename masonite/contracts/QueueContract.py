from abc import ABC, abstractmethod


class QueueContract(ABC):

    @abstractmethod
    def push(self): pass
