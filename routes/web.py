''' Web Routes '''
from app.http.providers.routes import Get, Post
from app.http.controllers.WelcomeController import WelcomeController

routes = [
    Get().route('/', WelcomeController().show),
]
