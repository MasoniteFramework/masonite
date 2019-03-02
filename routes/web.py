"""Web Routes."""

from masonite.routes import Get

ROUTES = [
    Get().route('/', 'WelcomeController@show').name('welcome'),
]
