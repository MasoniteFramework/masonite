from tests import TestCase
from tests.integrations.app.SayHi import SayHello
from tests.integrations.app.GreetingService import GreetingService
from tests.integrations.app.User import User


class TestContainer(TestCase):
    def test_container_can_resolve_without_binding(self):
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

    def test_container_can_resolve_nested_dependencies_without_binding(self):
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
