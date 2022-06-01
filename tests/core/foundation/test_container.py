from typing import TYPE_CHECKING
from tests import TestCase
from tests.integrations.app.SayHi import SayHello
from tests.integrations.app.GreetingService import GreetingService
from tests.integrations.app.User import User

from src.masonite.exceptions import (
    StrictContainerException,
    MissingContainerBindingNotFound,
)

if TYPE_CHECKING:
    from src.masonite.foundation import Application

from src.masonite.foundation import Application


class SomeObject:

    class_attribute = 1

    def __init__(self, attribute):
        self.attribute = attribute


class SomeStringTypeHintedAppObject:
    def __init__(self, app: "Application"):
        self.app = app


class SomeAppObject:
    def __init__(self, app: Application):
        self.app = app


class TestContainer(TestCase):
    def tearDown(self):
        super().tearDown()
        # unbind container.test after each test
        self.application.objects.pop("container.test", None)

    def test_cannot_bind_module(self):
        from src.masonite import foundation

        with self.assertRaises(StrictContainerException):
            self.application.bind("container.test", foundation)

    def test_can_bind_object(self):
        obj = SomeObject("test")
        self.application.bind("container.test", obj)
        bound_obj = self.application.make("container.test")

        self.assertEqual(obj, bound_obj)
        self.assertEqual(obj.class_attribute, 1)
        self.assertEqual(obj.attribute, "test")

        bound_obj.attribute = "test_updated"

        self.assertEqual(
            self.application.make("container.test").attribute, "test_updated"
        )

    def test_can_override_bound_objects(self):
        obj = SomeObject("test")
        self.application.bind("container.test", obj)
        other_obj = SomeObject("test")
        self.application.bind("container.test", other_obj)
        self.assertEqual(self.application.make("container.test"), other_obj)

    def test_container_has_binding(self):
        self.assertFalse(self.application.has("SomeUnexistingBinding"))
        self.assertFalse(self.application.has(TestContainer))

        self.application.bind("container.test", 1)
        self.assertTrue(self.application.has("container.test"))

    def test_container_cannot_resolve_unbound_objects_which_are_not_classes(self):
        with self.assertRaises(MissingContainerBindingNotFound):
            self.application.make("container.test")

    def test_container_can_resolve_classes_without_binding(self):
        # First pass - not in container
        self.assertFalse(self.application.has(SayHello))
        say_hello = self.application.make(SayHello)
        self.assertIsInstance(say_hello, SayHello)

        # Second pass - we still haven't bound it after the above
        self.assertFalse(self.application.has(SayHello))
        say_hello2 = self.application.make(SayHello)
        self.assertIsInstance(say_hello2, SayHello)

        # Container should have resolved different objects
        self.assertIsNot(say_hello, say_hello2)

    def test_container_can_resolve_nested_class_dependencies_without_binding(self):
        # There's an unbound dependency in __init__()
        service = self.application.make(GreetingService)

        # There's another unbound dependency in handle()
        # And that unbound dependency also has an unbound
        # dependency in its __init()
        result = self.application.resolve(getattr(service, "handle"))

        self.assertIsInstance(result, User)
        self.assertEqual("Jack Sparrow", result.name)

        # All resolved but none bound
        self.assertFalse(self.application.has(GreetingService))
        self.assertFalse(self.application.has(SayHello))
        self.assertFalse(self.application.has(User))

    def test_can_collect_bindings(self):
        bindings = self.application.collect("*.location")
        self.assertGreater(len(bindings), 0)
        self.assertIn("config.location", bindings.keys())

    def test_can_resolve_annotated_parameter(self):
        from src.masonite.response import Response

        def my_method(response: Response):
            return "ok"

        self.application.resolve(my_method)

    def test_can_resolve_class_with_str_type_hinted_parameters(self):
        def my_method(test: SomeStringTypeHintedAppObject):
            return test

        with self.assertRaises(TypeError):
            self.application.resolve(my_method)

    def test_can_resolve_class_with_str_type_hinted_parameters_and_pass_parameter(self):
        def my_method(test: SomeStringTypeHintedAppObject):
            return test

        obj = self.application.resolve(my_method, 1)
        self.assertEquals(obj.app + 1, 2)

    def test_can_resolve_class_with_type_hinted_parameters(self):
        def my_method(test: SomeAppObject):
            return test.app

        self.application.resolve(my_method)
