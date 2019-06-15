"""Web Routes."""

from masonite.routes import Get, Post, Redirect, RouteGroup, Patch


ROUTES = [
    Get().route('/test', None).middleware('auth'),
    Get().route('/queue', 'TestController@queue'),
    Redirect('/redirect', 'test'),
    Get().domain('test').route('/test', None).middleware('auth'),
    Get().domain('test').route('/unit/test', 'TestController@testing').middleware('auth'),
    Get().domain('test').route('/test/route', 'TestController@testing'),
    Get('/json_response', 'TestController@json_response'),
    Post('/test/post/route', 'TestController@post_test'),
    Get('/login', 'TestController@testing').name('login'),
    Get('/test/param/@id', 'TestController@testing'),
    Post('/test/json/response/@id', 'TestController@json'),
    Get('/test/set/test/session', 'TestController@session'),
    RouteGroup([
        Get('/test/1', 'TestController@show'),
        Get('/test/2', 'TestController@show')
    ], prefix='/example'),
    RouteGroup([
        Get('/test/get', 'UnitTestController@show'),
        Get('/test/param/@post_id', 'UnitTestController@param'),
        Post('/test/post', 'UnitTestController@store').middleware('test'),
        Get('/test/get/params', 'UnitTestController@get_params').name('get.params'),
        Post('/test/params', 'UnitTestController@params'),
        Post('/test/user', 'UnitTestController@user'),
        Post('/test/json', 'UnitTestController@json'),
        Patch('/test/patch', 'UnitTestController@patch'),
    ], prefix="/unit")
]
