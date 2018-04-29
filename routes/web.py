from masonite.helpers.routes import group
from masonite.routes import Get


ROUTES = [
    Get().route('/test', None).middleware('auth'),
    Get().domain('test').route('/test', None).middleware('auth'),
    group('/example', [
        Get().route('/test/1', 'TestController@show'),
        Get().route('/test/2', 'TestController@show')
    ])
]
