import os
import unittest

from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.routes import Get
from masonite.testsuite.TestSuite import TestSuite, generate_wsgi


class ContainerTest(ServiceProvider):

    def boot(self, request: Request, get: Get):
        return request

    def testboot(self, request: Request, get: Get):
        return request


class ServiceProviderTest(ServiceProvider):

    def register(self):
        self.app.bind('Request', object)


class Mock1Command:
    pass


class Mock2Command:
    pass


ROUTE1 = Get().route('/url/here', None)
ROUTE2 = Get().route('/test/url', None)


class LoadProvider(ServiceProvider):

    def boot(self):
        self.routes([
            ROUTE1,
            ROUTE2
        ])

        self.http_middleware([
            object,
            object
        ])

        self.route_middleware({
            'route1': object,
            'route2': object,
        })

        self.migrations('directory/1', 'directory/2')

        self.assets({
            'storage/static': '/some/location'
        })

        self.commands(Mock1Command(), Mock2Command())


class TestServiceProvider(unittest.TestCase):

    def setUp(self):
        self.app = TestSuite().create_container().container
        self.app.resolve_parameters = True
        self.provider = ServiceProvider()
        self.provider.load_app(self.app).register()
        self.load_provider = LoadProvider()
        self.load_provider.load_app(self.app).boot()

    def test_service_provider_loads_app(self):
        self.assertEqual(self.provider.app, self.app)

    def test_can_call_container_with_self_parameter(self):
        self.app.bind('Request', Request({}))
        self.app.bind('Get', Get())

        self.assertEqual(self.app.resolve(ContainerTest().boot), self.app.make('Request'))

    def test_can_call_container_with_annotations_from_variable(self):
        request = Request(generate_wsgi())

        self.app.bind('Request', request)
        self.app.bind('Get', Get().route('url', None))

        self.assertEqual(self.app.resolve(ContainerTest().testboot), self.app.make('Request'))

    def test_can_load_routes_into_container(self):
        self.assertTrue(len(self.app.make('WebRoutes')) > 2)
        self.assertEqual(self.app.make('WebRoutes')[-2:], [ROUTE1, ROUTE2])

    def test_can_load_http_middleware_into_container(self):
        self.assertEqual(self.app.make('HttpMiddleware')[-2:], [object, object])

    def test_can_load_route_middleware_into_container(self):
        self.assertEqual(self.app.make('RouteMiddleware')['route1'], object)
        self.assertEqual(self.app.make('RouteMiddleware')['route2'], object)

    def test_can_load_migrations_into_container(self):
        self.assertEqual(len(self.app.collect('*MigrationDirectory')), 2)

    def test_can_load_assets_into_container(self):
        self.assertEqual(self.app.make('Storage').STATICFILES['storage/static'], '/some/location')

    def test_can_load_commands_into_container(self):
        self.assertTrue(self.app.make('Mock1Command'))
        self.assertTrue(self.app.make('Mock2Command'))

    def test_can_load_publishing(self):
        self.load_provider.publishes({
            'from/directory': 'to/directory'
        })
        self.assertEqual(self.load_provider._publishes, {'from/directory': 'to/directory'})
        # self.assertTrue(self.app.make('Mock2Command'))

    def test_provider_can_publish_with_tags(self):
        self.load_provider.publishes({
            'from/directory': 'to/directory'
        }, tag='config')
        self.assertEqual(self.load_provider._publishes, {'from/directory': 'to/directory'})
        self.assertEqual(self.load_provider._publish_tags.get('config'), {'from/directory': 'to/directory'})

    def test_provider_can_publish(self):
        self.load_provider.publishes({
            os.path.join(os.getcwd(), 'storage/append_from.txt'): 'storage/append_to.txt'
        }, tag='config')

        self.load_provider.publish()
        os.remove(os.path.join(os.getcwd(), 'storage/append_to.txt'))

    def test_provider_can_publish_a_tag(self):
        self.load_provider.publishes({
            os.path.join(os.getcwd(), 'storage/append_from.txt'): 'storage/append_to.txt'
        }, tag='config')

        self.load_provider.publish(tag='config')
        os.remove(os.path.join(os.getcwd(), 'storage/append_to.txt'))
