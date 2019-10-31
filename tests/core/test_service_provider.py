import os
import unittest

from src.masonite.provider import ServiceProvider
from src.masonite.request import Request
from src.masonite.routes import Get
from src.masonite.testing import TestCase, generate_wsgi


class ContainerTest(ServiceProvider):

    def boot(self, request: Request, get: Get):
        return request

    def testboot(self, request: Request, get: Get):
        return request


class ServiceProviderTest(ServiceProvider):

    def register(self):
        self.container.bind('Request', object)


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


class TestServiceProvider(TestCase):

    def setUp(self):
        super().setUp()
        self.container.resolve_parameters = True
        self.provider = ServiceProvider()
        self.provider.load_app(self.container).register()
        self.load_provider = LoadProvider()
        self.load_provider.load_app(self.container).boot()

    def test_service_provider_loads_app(self):
        self.assertEqual(self.provider.app, self.container)

    def test_can_call_container_with_self_parameter(self):
        self.container.bind('Request', Request({}))
        self.container.bind('Get', Get())

        self.assertEqual(self.container.resolve(ContainerTest().boot), self.container.make('Request'))

    def test_can_call_container_with_annotations_from_variable(self):
        request = Request(generate_wsgi())

        self.container.bind('Request', request)
        self.container.bind('Get', Get().route('url', None))

        self.assertEqual(self.container.resolve(ContainerTest().testboot), self.container.make('Request'))

    def test_can_load_routes_into_container(self):
        self.assertTrue(len(self.container.make('WebRoutes')) > 2)
        self.assertEqual(self.container.make('WebRoutes')[-2:], [ROUTE1, ROUTE2])

    def test_can_load_http_middleware_into_container(self):
        self.assertEqual(self.container.make('HttpMiddleware')[-2:], [object, object])

    def test_can_load_route_middleware_into_container(self):
        self.assertEqual(self.container.make('RouteMiddleware')['route1'], object)
        self.assertEqual(self.container.make('RouteMiddleware')['route2'], object)

    def test_can_load_migrations_into_container(self):
        self.assertEqual(len(self.container.collect('*MigrationDirectory')), 12)

    def test_can_load_assets_into_container(self):
        self.assertEqual(self.container.make('staticfiles')['storage/static'], '/some/location')

    def test_can_load_commands_into_container(self):
        self.assertTrue(self.container.make('Mock1Command'))
        self.assertTrue(self.container.make('Mock2Command'))

    def test_can_load_publishing(self):
        self.load_provider.publishes({
            'from/directory': 'to/directory'
        })
        self.assertEqual(self.load_provider._publishes, {'from/directory': 'to/directory'})
        # self.assertTrue(self.container.make('Mock2Command'))

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
