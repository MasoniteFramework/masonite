from src.masonite.routes import Get, Post
from src.masonite.request import Request
from src.masonite.testing import TestCase, generate_wsgi
import unittest


class TestRequestRoutes(TestCase):

    def setUp(self):
        super().setUp()
        self.request = self.container.make('Request').load_environ(generate_wsgi()).key(
            'NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY=')

        self.request.activate_subdomains()

    def test_get_initialized(self):
        self.assertTrue(callable(Get))
        self.assertTrue(callable(Post))

    def test_get_sets_route(self):
        self.assertTrue(Get().route('test', None))

    def test_sets_name(self):
        get = Get().route('test', None).name('test')

        self.assertEqual(get.named_route, 'test')

    def test_loads_request(self):
        get = Get().route('test', None).name('test').load_request('test')

        self.assertEqual(get.request, 'test')

    def test_loads_middleware(self):
        get = Get().route('test', None).middleware('auth', 'middleware')

        self.assertEqual(get.list_middleware, ['auth', 'middleware'])

    def test_method_type(self):
        self.assertEqual(Post().method_type, ['POST'])
        self.assertEqual(Get().method_type, ['GET'])

    def test_method_type_sets_domain(self):
        get = Get().domain('test')
        post = Post().domain('test')

        self.assertEqual(get.required_domain, 'test')
        self.assertEqual(post.required_domain, 'test')

    def test_method_type_has_required_subdomain(self):
        get = Get().domain('test')
        post = Get().domain('test')

        self.request.environ['HTTP_HOST'] = 'test.localhost:8000'

        get.request = post.request = self.request

        self.assertEqual(get.has_required_domain(), True)
        self.assertEqual(post.has_required_domain(), True)

    def test_method_type_has_required_subdomain_with_asterick(self):
        

        self.request.environ['HTTP_HOST'] = 'test.localhost:8000'

        self.request.activate_subdomains()

        get = Get().domain('*')
        post = Get().domain('*')

        get.request = self.request
        post.request = self.request

        self.assertEqual(get.has_required_domain(), True)
        self.assertEqual(post.has_required_domain(), True)

    def test_request_sets_subdomain_on_get(self):
        

        self.request.environ['HTTP_HOST'] = 'test.localhost:8000'

        self.request.activate_subdomains()

        get = Get().domain('*')
        post = Get().domain('*')

        get.request = self.request
        post.request = self.request

        get.has_required_domain()
        self.assertEqual(self.request.param('subdomain'), 'test')

    def test_route_changes_module_location(self):
        get = Get().module('app.test')
        self.assertEqual(get.module_location, 'app.test')
