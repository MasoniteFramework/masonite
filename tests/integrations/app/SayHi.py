from src.masonite.queues import Queueable


class SayHello(Queueable):
    def handle(self):
        print("hello there")
