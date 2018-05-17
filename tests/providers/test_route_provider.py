from masonite.app import App
from masonite.routes import Route
from masonite.request import Request
from masonite.providers.RouteProvider import RouteProvider
from masonite.view import View
from masonite.helpers.routes import get
from masonite.testsuite.TestSuite import generate_wsgi


class TestRouteProvider:

    def setup_method(self):
        self.app = App()
        self.app.bind('Environ', generate_wsgi())
        self.app.bind('WebRoutes', [])
        self.app.bind('Route', Route(self.app.make('Environ')))
        self.app.bind('Request', Request(self.app.make('Environ')).load_app(self.app))
        self.app.bind('Headers', [])
        self.app.bind('HttpMiddleware', [])
        view = View(self.app)
        self.app.bind('View', view.render)
        self.provider = RouteProvider()
        self.provider.app = self.app

     
    def test_controller_that_returns_a_view(self):
        self.app.make('Route').url = '/view'
        self.app.bind('WebRoutes', [get('/view', Controller.returns_a_view)])

        self.provider.boot(
            self.app.make('WebRoutes'),
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make('Environ'),
            self.app.make('Headers'),
        )

        assert self.app.make('Response') == 'hey'

    def test_controller_does_not_return_with_non_matching_end_slash(self):
        self.app.make('Route').url = '/view'
        self.app.bind('WebRoutes', [get('/view/', Controller.returns_a_view)])

        self.provider.boot(
            self.app.make('WebRoutes'),
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make('Environ'),
            self.app.make('Headers'),
        )

        assert self.app.make('Response') == 'Route not found. Error 404'


    def test_provider_runs_through_routes(self):
        self.app.make('Route').url = '/test'
        self.app.bind('WebRoutes', [get('/test', Controller.show)])

        self.provider.boot(
            self.app.make('WebRoutes'),
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make('Environ'),
            self.app.make('Headers'),
        )

        assert self.app.make('Request').header('Content-Type') == 'text/html; charset=utf-8'


    def test_sets_request_params(self):
        self.app.make('Route').url = '/test/1'
        self.app.bind('WebRoutes', [get('/test/@id', Controller.show)])

        self.provider.boot(
            self.app.make('WebRoutes'),
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make('Environ'),
            self.app.make('Headers'),
        )

        assert self.app.make('Request').param('id') == '1'
    
    def test_route_subdomain_ignores_routes(self):
        self.app.make('Route').url = '/test'
        self.app.make('Environ')['HTTP_HOST'] = 'subb.domain.com'
        self.app.bind('WebRoutes', [get('/test', Controller.show)])

        self.provider.boot(
            self.app.make('WebRoutes'),
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make('Environ'),
            self.app.make('Headers'),
        )

        assert self.app.make('Response') == 'Route not found. Error 404'
    
    def test_controller_returns_json_response_for_dict(self):
        self.app.make('Route').url = '/view'
        self.app.bind('WebRoutes', [get('/view', Controller.returns_a_dict)])

        self.provider.boot(
            self.app.make('WebRoutes'),
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make('Environ'),
            self.app.make('Headers'),
        )

        assert self.app.make('Response') == '{"id": 1}'
        assert self.app.make('Request').header('Content-Type') == 'application/json; charset=utf-8'

class Controller:

    def show():
        return 'test'
    
    def returns_a_view(View):
        return View('index')

    def returns_a_dict():
        return {'id': 1}

class Middleware:

    def before(): pass

    def after(): pass
