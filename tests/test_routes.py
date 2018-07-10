from masonite.routes import Route
from masonite.request import Request
from masonite.routes import Get, Post, Put, Patch, Delete, RouteGroup
from masonite.helpers.routes import group
from masonite.testsuite.TestSuite import generate_wsgi


class TestRoutes:

    def setup_method(self):
        self.route = Route(generate_wsgi())
        self.request = Request(generate_wsgi())

    def test_route_is_callable(self):
        assert callable(Get)
        assert callable(Post)
        assert callable(Put)
        assert callable(Patch)
        assert callable(Delete)


    def test_route_get_returns_output(self):
        assert self.route.get('url', 'output') == 'output'

    def test_route_is_not_post(self):
        assert self.route.is_post() == False

    def test_route_is_post(self):
        self.route.environ['REQUEST_METHOD'] = 'POST'
        assert self.route.is_post() == True


    def test_compile_route_to_regex(self):
        assert self.route.compile_route_to_regex(Get().route('test/route', None)) == '^test\\/route\\/$'
        assert self.route.compile_route_to_regex(Get().route(
            'test/@route', None)) == '^test\\/(\\w+)\\/$'

        assert self.route.compile_route_to_regex(Get().route(
            'test/@route:int', None)) == '^test\\/(\\d+)\\/$'

        assert self.route.compile_route_to_regex(Get().route(
            'test/@route:string', None)) == '^test\\/([a-zA-Z]+)\\/$'

    def test_route_gets_controllers(self):
        assert Get().route('test/url', 'TestController@show')
        assert Get().route('test/url', '/app.http.test_controllers.TestController@show')


    def test_route_doesnt_break_on_incorrect_controller(self):
        assert Get().route('test/url', 'BreakController@show')


    def test_group_route(self):
        routes = group('/example', [
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ])

        assert routes[0].route_url == '/example/test/1'
        assert routes[1].route_url == '/example/test/2'

    def test_group_route_sets_middleware(self):
        routes = group('/example', [
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ])

        assert routes[0].route_url == '/example/test/1'

        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], middleware=['auth', 'user'])

        assert isinstance(routes, list)

        assert routes[0].list_middleware == ('auth', 'user')

    def test_group_route_sets_domain(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], domain=['www'])

        assert routes[0].required_domain == ['www']

    def test_group_route_sets_prefix(self):
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show'),
            Get().route('/test/2', 'TestController@show')
        ], prefix='/dashboard')

        assert routes[0].route_url == '/dashboard/test/1'

    def test_group_route_sets_name(self):
        look_for = []
        routes = RouteGroup([
            Get().route('/test/1', 'TestController@show').name('create'),
            Get().route('/test/2', 'TestController@show').name('edit')
        ], name='post.')

        assert routes[0].named_route == 'post.create'
        assert routes[1].named_route == 'post.edit'
