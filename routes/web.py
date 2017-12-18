''' Web Routes '''
from app.http.providers.routes import Get, Post
from app.http.controllers.WelcomeController import WelcomeController

ROUTES = [
    Get().route('/', WelcomeController().show),
]
