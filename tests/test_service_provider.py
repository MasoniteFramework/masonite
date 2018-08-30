import inspect

from masonite.provider import ServiceProvider
from masonite.app import App
from masonite.request import Request
from masonite.routes import Get
from masonite.testsuite.TestSuite import generate_wsgi


class ContainerTest(ServiceProvider):

    def boot(self, Request, Get):
        return Request

    def testboot(self, request: Request, Get: Get):
        return request

class ServiceProviderTest(ServiceProvider):

    def register(self):
        self.app.bind('Request', object)

class TestServiceProvider:

    def setup_method(self):
        self.app = App()
        self.provider = ServiceProviderTest()
        self.provider.load_app(self.app).register()
        self.provider.boot()

    def test_service_provider_loads_app(self):
        assert self.provider.app == self.app

    def test_can_call_container_with_self_parameter(self):
        self.app.bind('Request', object)
        self.app.bind('Get', object)

        assert self.app.resolve(ContainerTest().boot) == self.app.make('Request')

    def test_can_call_container_with_annotations_from_variable(self):
        request = Request(generate_wsgi())

        self.app.bind('Request', request)
        self.app.bind('Get', Get().route('url', None))

        assert self.app.resolve(ContainerTest().testboot) == self.app.make('Request')
    
    def test_can_call_container_with_annotation_with_self_parameter(self):
        self.app.bind('Request', Request)
        self.app.bind('Get', Get().route('url', None))

        assert self.app.resolve(ContainerTest().testboot) == self.app.make('Request')
        
    def test_service_provider_sets_on_app_object(self):
        assert 'Request' in self.app.providers 
        assert self.app.make('Request') == object
