from tests import TestCase
from src.masonite.routes import Route
from src.masonite.controllers import Controller
from src.masonite.exceptions import RouteNotFoundException


class TestController(Controller):
    def simple(self):
        1 / 0

    def http(self):
        raise RouteNotFoundException()


class TestExceptionHandlerInDebug(TestCase):
    def setUp(self):
        super().setUp()
        self.handler = self.application.make("exception_handler")
        self.setRoutes(
            Route.get("/simple", TestController.simple),
            Route.get("/http", TestController.http),
        )
        # enable exceptions handling during all the tests of this class
        # because it is what is tested here
        self.withExceptionsHandling()

    def test_that_exception_event_is_fired(self):
        # with self.debugMode():
        #     self.get("/simple")
        pass

    def test_raising_simple_exception_renders_debug_error_page(self):
        with self.debugMode():
            self.get("/simple").assertError().assertContains(
                "ZeroDivisionError"
            ).assertContains("Exceptionite")

    def test_raising_http_exception_renders_debug_error_page(self):
        with self.debugMode():
            self.get("/http").assertError().assertContains(
                "RouteNotFoundException"
            ).assertContains("Exceptionite")

    def test_raising_exception_output_stack_trace_to_console(self):
        with self.debugMode():
            self.get("/simple")
            self.assertConsoleOutputContains(
                "ZeroDivisionError: division by zero"
            ).assertConsoleOutputContains("Stack Trace")

    def test_accepting_json_returns_debug_error_payload(self):
        with self.debugMode():
            self.withHeaders({"Accept": "application/json"}).get(
                "/simple"
            ).assertError().assertJsonPath("exception.type", "ZeroDivisionError")


class TestExceptionHandler(TestCase):
    """Test error handling in production mode, debug is False."""

    def setUp(self):
        super().setUp()
        self.handler = self.application.make("exception_handler")
        self.setRoutes(Route.get("/simple", TestController.simple))
        # enable exceptions handling during all the tests of this class
        # because it is what is tested here
        self.withExceptionsHandling()

    def test_that_exception_event_is_fired(self):
        pass

    def test_raising_simple_exception_renders_500_error_template(self):
        with self.debugMode(False):
            self.get("/simple").assertError().assertContains("Error 500")

    def test_raising_http_exception_renders_404_error_page(self):
        with self.debugMode(False):
            self.get("/http").assertNotFound().assertContains("Page Not Found")

    def test_raising_exception_does_not_output_stack_trace_to_console(self):
        with self.debugMode(False):
            self.get("/simple")
            self.assertConsoleEmpty()

    def test_accepting_json_returns_500_error_payload(self):
        with self.debugMode(False):
            self.withHeaders({"Accept": "application/json"}).get(
                "/simple"
            ).assertError().assertJson({"status": 500, "message": "division by zero"})
