import unittest

from masonite.app import App
from masonite.autoload import Autoload
from masonite.exceptions import (AutoloadContainerOverwrite, ContainerError,
                                 InvalidAutoloadPath)
from masonite.request import Request


class TestAutoload(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_autoload_loads_from_directories(self):
        Autoload(self.app).load(['app/http/controllers'])
        self.assertTrue(self.app.make('TestController'))

    def test_autoload_instantiates_classes(self):
        classes = Autoload().collect(['app/http/test_controllers'], instantiate=True)
        self.assertTrue(classes['TestController'].test)

    def test_autoload_loads_from_directories_with_trailing_slash_raises_exception(self):
        with self.assertRaises(InvalidAutoloadPath):
            Autoload(self.app).load(['app/http/controllers/'])

    def test_autoload_raises_exception_with_no_container(self):
        with self.assertRaises(ContainerError):
            Autoload().load(['app/http/controllers/'])

    def test_autoload_collects_classes(self):
        classes = Autoload().collect(['app/http/controllers'])
        self.assertIn('TestController', classes)
        self.assertNotIn('Command', classes)

    def test_autoload_loads_from_directories_and_instances(self):
        classes = Autoload().instances(['app/http/controllers'], object)
        self.assertIn('TestController', classes)
        self.assertNotIn('Command', classes)

    def test_autoload_loads_not_only_from_app_from_directories_and_instances(self):
        classes = Autoload().instances(['app/http/controllers'], object, only_app=False)
        self.assertIn('TestController', classes)

    def test_autoload_does_not_instantiate_classes(self):
        classes = Autoload().instances(['app/http/controllers'], object)
        with self.assertRaises(AttributeError):
            self.assertTrue(classes['TestController'].test, True)

    def test_collects_classes_only_in_app(self):
        classes = Autoload().collect(['app/http/controllers'], only_app=False)
        self.assertIn('TestController', classes)

    def test_autoload_throws_exception_when_binding_key_that_already_exists(self):
        self.app.bind('Request', Request(None))
        with self.assertRaises(AutoloadContainerOverwrite):
            Autoload(self.app).load(['app/http/test_controllers'])
