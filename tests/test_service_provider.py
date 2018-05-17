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

def test_service_provider_loads_app():
    app = App()
    provider = ServiceProvider()
    provider.load_app(app).boot()

    assert provider.app == app


def test_service_provider_sets_on_app_object():
    app = App()
    provider = ServiceProvider()
    provider.load_app(app).register()

    assert 'Request' in app.providers 
    assert app.make('Request') == object


def test_can_call_container_with_self_parameter():
    app = App()

    app.bind('Request', object)
    app.bind('Get', object)

    assert app.resolve(ContainerTest().boot) == app.make('Request')


wsgi_request = generate_wsgi()


def test_can_call_container_with_annotations_from_variable():
    app = App()

    request = Request(wsgi_request)

    app.bind('Request', request)
    app.bind('Get', Get().route('url', None))

    assert app.resolve(ContainerTest().testboot) == app.make('Request')


def test_can_call_container_with_annotation_with_self_parameter():
    app = App()

    app.bind('Request', Request)
    app.bind('Get', Get().route('url', None))

    assert app.resolve(ContainerTest().testboot) == app.make('Request')
