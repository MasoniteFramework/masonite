from masonite.testsuite.TestSuite import TestSuite


class TestTestSuite:

    def setup_method(self):
        self.suite = TestSuite().create_container()
        self.container = self.suite.get_container()

    def test_testsuite_creates_container(self):
        assert self.container.make('Request')

    def test_testsuite_should_return_route_exists(self):
        assert self.suite.route('/test').exists() is True

    def test_testsuite_route_should_return_bool_if_has_middleware(self):
        assert self.suite.route('/test').has_middleware('auth') is True
        assert self.suite.route('/test').has_middleware('none') is False
