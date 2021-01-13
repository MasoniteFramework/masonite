"""Web Routes."""

# from src.masonite.routes import Get, Post, Redirect, RouteGroup, Patch, Options
from src.masonite.routes import Route

Route.get('/test', None).middleware('auth')
Route.get('/bad/@id', 'WelcomeController@show')
Route.get('/bad', 'TestController@bad')
Route.get('/welcome', 'WelcomeController@show')
Route.get('/keyerror', 'TestController@keyerror')
Route.get('/queue', 'TestController@queue'),
Route.option('options', 'TestController@show'),
# Get().domain('test').route('/test', None).middleware('auth'),
# Get().domain('test').route('/unit/test', 'TestController@testing').middleware('auth'),
# Get().domain('test').route('/test/route', 'TestController@testing'),
# Redirect('/redirect', 'test'),
Route.get('/json_response', 'TestController@json_response'),
Route.get('/login', 'TestController@testing').name('login'),
Route.get('/v', 'TestController@v').name('v'),
Route.get('/', 'TestController@v').name('v'),
Route.get('/test/param/@id', 'TestController@testing'),
Route.post('/test/post/route', 'TestController@post_test'),
Route.post('/test/json/response/@id', 'TestController@json'),
Route.get('/test/set/test/session', 'TestController@session'),
Route.get('/test/mail', 'TestController@mail'),
Route.group(
    Route.get('/test/1', 'TestController@show'),
    Route.get('/test/2', 'TestController@show'),
    prefix="/example"
)
Route.group(
    Route.get('/test/get', 'UnitTestController@show'),
    Route.get('/test/param/@post_id', 'UnitTestController@param'),
    Route.post('/test/post', 'UnitTestController@store').middleware('test'),
    Route.get('/test/get/params', 'UnitTestController@get_params').name('get.params'),
    Route.post('/test/params', 'UnitTestController@params'),
    Route.post('/test/user', 'UnitTestController@user'),
    Route.post('/test/json', 'UnitTestController@json'),
    Route.get('/test/json/response', 'UnitTestController@response'),
    Route.post('/test/json/validate', 'UnitTestController@validate'),
    Route.get('/test/json/multi', 'UnitTestController@multi'),
    Route.get('/test/json/multi_count', 'UnitTestController@multi_count'),
    Route.patch('/test/patch', 'UnitTestController@patch'),
    prefix="/unit"
)
# RouteGroup([
#     Get('/deep/1', 'DeepController@show'),
# ], prefix='/example', namespace='subdirectory.deep.'),

ROUTES = [

]

# from src.masonite.auth import Auth 
# ROUTES += Auth.routes()
