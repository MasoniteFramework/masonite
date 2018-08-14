from masonite.helpers.routes import group
from masonite.routes import Get, Post


ROUTES = [
    Get().route('/test', None).middleware('auth'),
    Get().domain('test').route('/test', None).middleware('auth'),
    Get().domain('test').route('/unit/test', 'TestController@testing').middleware('auth'),
    Get().domain('test').route('/test/route', 'TestController@testing'),
    Post().route('/test/post/route', 'TestController@post_test'),
    Get().route('/login', 'TestController@testing').name('login'),
    Get().route('/test/param/@id', 'TestController@testing'),
    group('/example', [
        Get().route('/test/1', 'TestController@show'),
        Get().route('/test/2', 'TestController@show')
    ])
]
