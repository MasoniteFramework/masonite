from masonite.providers import StatusCodeProvider
from masonite.request import Request
from masonite.view import View
from masonite.app import App
from masonite.providers.StatusCodeProvider import ServerErrorExceptionHook

class TestStatusCode:

    def setup_method(self):
        self.app = App()
        self.app.bind('StatusCode', '404 Not Found')
        self.app.bind('Request', Request(None).load_app(self.app))
        self.app.bind('ViewClass', View(self.app))
        self.app.bind('View', self.app.make('ViewClass').render)
        self.provider = StatusCodeProvider().load_app(self.app).boot()
    
    def test_provider_returns_masonite_view(self):
        assert '404 Not Found' in self.app.make('Response')
        assert self.app.make('Headers')
    
    def test_provider_returns_none_on_200_OK(self):
        self.provider = StatusCodeProvider().load_app(self.app).boot()
        assert self.provider is None

class MockApplicationConfig:
    DEBUG = 'True'

class TestServerErrorExceptionHook:

    def setup_method(self):
        self.app = App()
        self.app.bind('Request', Request(None).load_app(self.app))
        self.app.bind('Application', MockApplicationConfig)
        self.app.bind('ViewClass', View(self.app))
        self.app.bind('View', self.app.make('ViewClass').render)
        self.hook = ServerErrorExceptionHook().load(self.app)

    def test_response_is_set_when_app_debug_is_true(self):
        assert self.hook is None
    
    def test_no_response_set_when_app_debug_is_false(self):
        application = MockApplicationConfig
        application.DEBUG = False
        self.app.bind('Application', application)
        assert self.hook == ServerErrorExceptionHook().load(self.app) is None