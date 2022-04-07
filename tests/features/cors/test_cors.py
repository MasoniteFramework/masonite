from tests import TestCase


class TestCors(TestCase):
    def setUp(self):
        super().setUp()
        self.cors = self.application.make("cors")

    def test_todo(self):
        pass
