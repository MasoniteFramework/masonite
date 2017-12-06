from app.http.providers.routes import Get
from resources.views.home import Home
from app.http.providers.view import view
from app.http.controllers.WelcomeController import WelcomeController

routes = [
    Get().route('/home', WelcomeController().show())
]