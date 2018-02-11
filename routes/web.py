from masonite.routes import Get
ROUTES = [
    Get().route('/test', None).middleware('auth')
]