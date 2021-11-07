from .Facade import Facade


class Session(metaclass=Facade):
    key = "session"
