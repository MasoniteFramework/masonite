"""Web Routes."""

from src.masonite.routes import Get, Post, Redirect, RouteGroup, Patch, Options


ROUTES = [
    Get().route('/test', None).middleware('auth'),
    Get('/bad', 'TestController@bad'),
    Get('/welcome', 'WelcomeController@show'),
    Get('/keyerror', 'TestController@keyerror'),
    Get().route('/queue', 'TestController@queue'),
    Options('options', 'TestController@show'),
    Redirect('/redirect', 'test'),
    Get().domain('test').route('/test', None).middleware('auth'),
    Get().domain('test').route('/unit/test', 'TestController@testing').middleware('auth'),
    Get().domain('test').route('/test/route', 'TestController@testing'),
    Get('/json_response', 'TestController@json_response'),
    Post('/test/post/route', 'TestController@post_test'),
    Get('/login', 'TestController@testing').name('login'),
    Get('/v', 'TestController@v').name('v'),
    Get('/', 'TestController@v').name('v'),
    Get('/test/param/@id', 'TestController@testing'),
    Post('/test/json/response/@id', 'TestController@json'),
    Get('/test/set/test/session', 'TestController@session'),
    Get('/test/mail', 'TestController@mail'),
    RouteGroup([
        Get('/test/1', 'TestController@show'),
        Get('/test/2', 'TestController@show')
    ], prefix='/example'),
    RouteGroup([
        Get('/deep/1', 'DeepController@show'),
    ], prefix='/example', namespace='subdirectory.deep.'),
    RouteGroup([
        Get('/test/get', 'UnitTestController@show'),
        Get('/test/param/@post_id', 'UnitTestController@param'),
        Post('/test/post', 'UnitTestController@store').middleware('test'),
        Get('/test/get/params', 'UnitTestController@get_params').name('get.params'),
        Post('/test/params', 'UnitTestController@params'),
        Post('/test/user', 'UnitTestController@user'),
        Post('/test/json', 'UnitTestController@json'),
        Get('/test/json/response', 'UnitTestController@response'),
        Post('/test/json/validate', 'UnitTestController@validate'),
        Get('/test/json/multi', 'UnitTestController@multi'),
        Get('/test/json/multi_count', 'UnitTestController@multi_count'),
        Patch('/test/patch', 'UnitTestController@patch'),
    ], prefix="/unit")
]

from src.masonite.auth import Auth 
ROUTES += Auth.routes()
