from masonite.routes import Route
from masonite.request import Request
from masonite.routes import Get, Post, Put, Patch, Delete
from masonite.helpers.routes import group
from masonite.testsuite.TestSuite import generate_wsgi


ROUTE = Route(generate_wsgi())
REQUEST = Request(generate_wsgi())


def test_route_is_callable():
    assert callable(Get)
    assert callable(Post)
    assert callable(Put)
    assert callable(Patch)
    assert callable(Delete)


def test_route_get_returns_output():
    assert ROUTE.get('url', 'output') == 'output'


def test_route_is_not_post():
    assert ROUTE.is_post() == False


def test_route_is_post():
    ROUTE.environ['REQUEST_METHOD'] = 'POST'
    assert ROUTE.is_post() == True


def test_compile_route_to_regex():
    assert ROUTE.compile_route_to_regex(Get().route('test/route', None)) == '^test\\/route\\/$'
    assert ROUTE.compile_route_to_regex(Get().route(
        'test/@route', None)) == '^test\\/(\\w+)\\/$'

    assert ROUTE.compile_route_to_regex(Get().route(
        'test/@route:int', None)) == '^test\\/(\\d+)\\/$'

    assert ROUTE.compile_route_to_regex(Get().route(
        'test/@route:string', None)) == '^test\\/([a-zA-Z]+)\\/$'


def test_route_url_list():
    assert ROUTE.generated_url_list() == ['route']


def test_route_gets_controllers():
    assert Get().route('test/url', 'TestController@show')
    assert Get().route('test/url', '/app.http.test_controllers.TestController@show')


def test_route_doesnt_break_on_incorrect_controller():
    assert Get().route('test/url', 'BreakController@show')


def test_group_route():
    routes = group('/example', [
        Get().route('/test/1', 'TestController@show'),
        Get().route('/test/2', 'TestController@show')
    ])

    assert routes[0].route_url == '/example/test/1'
    assert routes[1].route_url == '/example/test/2'
