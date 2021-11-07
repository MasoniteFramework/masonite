from tests import TestCase

from src.masonite.loader.Loader import Loader
from src.masonite.exceptions import LoaderNotFound

OBJ_1 = "test"


class TestLoader(TestCase):
    def setUp(self):
        super().setUp()
        self.loader = Loader()

    def test_get_objects(self):
        objects = self.loader.get_objects("tests.features.loader.test_loader")
        self.assertIsInstance(objects, dict)
        self.assertEqual(objects.get("OBJ_1"), "test")
        self.assertEqual(objects.get("Loader"), Loader)

    def test_get_objects_for_unexisting_path(self):
        objects = self.loader.get_objects("test.not.existing.path")
        self.assertIsNone(objects)

    def test_get_parameters(self):
        objects = self.loader.get_parameters("tests.features.loader.test_loader")
        self.assertIsInstance(objects, dict)
        self.assertEqual(objects.get("OBJ_1"), "test")
        self.assertEqual(len(objects.keys()), 1)

    def test_find_all(self):
        from masoniteorm.models import Model
        from tests.integrations.app.User import User

        objects = self.loader.find_all(Model, "tests.integrations.app")
        self.assertIsInstance(objects, dict)
        self.assertEqual(objects.get("User"), User)
        self.assertEqual(len(objects.keys()), 1)

    def test_find(self):
        from masoniteorm.models import Model
        from tests.integrations.app.User import User

        obj = self.loader.find(Model, "tests.integrations.app", "User")
        self.assertEqual(obj, User)

    def test_find_methods_raise_exception_if_specified(self):
        from masoniteorm.models import Model

        with self.assertRaises(LoaderNotFound):
            self.loader.find(
                Model, "test.not.existing.path", "User", raise_exception=True
            )

        with self.assertRaises(LoaderNotFound):
            self.loader.find_all(Model, "test.not.existing.path", raise_exception=True)
