from masonite.routes import Get
ROUTES = [
    Get().route('/test', None).middleware('auth'),
    Get().domain('test').route('/test', None).middleware('auth'),
]