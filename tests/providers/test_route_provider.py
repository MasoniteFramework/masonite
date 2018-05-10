from masonite.app import App
from masonite.routes import Route
from masonite.request import Request
from masonite.providers.RouteProvider import RouteProvider
from masonite.view import View
from masonite.helpers.routes import get


class TestRouteProvider:

    def setup_method(self):
        self.app = App()
        WSGI_REQUEST = {
            'wsgi.version': (1, 0),
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
            'SERVER_SOFTWARE': 'gunicorn/19.7.1',
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'application=Masonite',
            'RAW_URI': '/',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'HTTP_HOST': '127.0.0.1:8000',
            'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'HTTP_UPGRADE_INSECURE_REQUESTS': '1',
            'HTTP_COOKIE': 'setcookie=value',
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
            'HTTP_ACCEPT_LANGUAGE': 'en-us',
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
            'HTTP_CONNECTION': 'keep-alive',
            'wsgi.url_scheme': 'http',
            'REMOTE_ADDR': '127.0.0.1',
            'REMOTE_PORT': '62241',
            'SERVER_NAME': '127.0.0.1',
            'SERVER_PORT': '8000',
            'PATH_INFO': '/',
            'SCRIPT_NAME': ''
        }
        self.app.bind('Environ', WSGI_REQUEST)
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
