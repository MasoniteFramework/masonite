from abc import ABC, abstractmethod


class UploadContract(ABC):

    @abstractmethod
    def accept(self):
        pass

    @abstractmethod
    def validate_extension(self):
        pass

    @abstractmethod
    def store(self):
        pass
