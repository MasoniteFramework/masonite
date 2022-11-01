from tests import TestCase

from src.masonite.helpers import app


class CountTestService:
    def __init__(self, count: int) -> None:
        self.count = count


class TestConfigHelper(TestCase):
    def test_can_get_app_container(self):
        self.assertEqual(app(), self.application)

    def test_can_get_resolve_bound_service(self):
        self.assertEqual(app("storage"), self.application.make("storage"))

    def test_can_resolve_service_with_parameters(self):
        self.application.bind("test.service", CountTestService)
        service = app("test.service", 5)
        self.assertIsInstance(service, CountTestService)
        self.assertEqual(service.count, 5)
