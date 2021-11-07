from tests import TestCase


class TestApplication(TestCase):
    def test_is_running_tests(self):
        self.assertTrue(self.application.is_running_tests())
