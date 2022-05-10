from .SayHi import SayHello
from .Repository import Repository


class GreetingService:
    def __init__(self, say_hello: SayHello):
        self.say_hello = say_hello

    def handle(self, repository: Repository):
        repository.user.name = "Jack Sparrow"
        return repository.user
