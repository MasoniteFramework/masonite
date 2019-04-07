from masonite.testsuite.TestSuite import TestSuite
import unittest

class TestTestSuite(unittest.TestCase):

    def setUp(self):
        self.suite = TestSuite().create_container()
        self.container = self.suite.get_container()

    def test_testsuite_creates_container(self):
        self.assertTrue(self.container.make('Request'))

    def test_testsuite_should_return_route_exists(self):
        self.assertTrue(self.suite.route('/test').exists())

    def test_testsuite_route_should_return_bool_if_has_middleware(self):
        self.assertTrue(self.suite.route('/test').has_middleware('auth'))
        self.assertFalse(self.suite.route('/test').has_middleware('none'))
