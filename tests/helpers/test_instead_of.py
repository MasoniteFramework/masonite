from masonite.request import Request
import unittest

class MockUser:
    pass

class InsteadOf:

    def __init__(self, cls, method):
        self.cls = cls
        self.method = method
    
    def _return(self, value):
        setattr(self.cls, self.method, value)
        return self.cls

class TestInsteadOf(unittest.TestCase):

    def test_instead_of_attribute(self):
        request = Request()

        InsteadOf(request, 'user')._return('awesome')

        self.assertEqual(request.user, 'awesome')

    def test_instead_of_with_method(self):
        request = Request()

        InsteadOf(request, 'user')._return(MockUser)

        self.assertIsInstance(request.user(), MockUser)