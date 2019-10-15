from masonite.testing import TestCase

class TestExceptionListener(TestCase):

    def setUp(self):
        super().setUp()

    def test_listener_fires(self):
        self.withExceptionHandling()
        self.assertEqual(self.get('/bad').request.error_thrown, True)

    def test_listener_doesnt_fire(self):
        self.withExceptionHandling()
        with self.assertRaises(AttributeError):
            self.assertEqual(self.get('/keyerror').request.error_thrown, True)
