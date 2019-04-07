from masonite.helpers import routes
from masonite.routes import Get, Post, Delete, Patch, Put
import unittest

class TestHelperUrl(unittest.TestCase):

    def test_get_sets_route(self):
        self.assertTrue(routes.get('test', None))
        self.assertIsInstance(routes.get('test', None), Get)

    def test_post_sets_route(self):
        self.assertTrue(routes.post('test', None))
        self.assertIsInstance(routes.post('test', None), Post)

    def test_put_sets_route(self):
        self.assertTrue(routes.put('test', None))
        self.assertIsInstance(routes.put('test', None), Put)

    def test_delete_sets_route(self):
        self.assertTrue(routes.delete('test', None))
        self.assertIsInstance(routes.delete('test', None), Delete)

    def test_patch_sets_route(self):
        self.assertTrue(routes.patch('test', None))
        self.assertIsInstance(routes.patch('test', None), Patch)
