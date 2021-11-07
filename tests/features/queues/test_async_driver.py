from tests import TestCase
from src.masonite.queues import Queueable
import os
import time


from tests.integrations.app.SayHi import SayHello


class TestAsyncDriver(TestCase):
    def test_async_push(self):
        self.application.make("queue").push(SayHello(), driver="async")
