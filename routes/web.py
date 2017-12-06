from app.http.providers.routes import Get
from resources.views.home import Home
from app.http.providers.view import view
from app.http.controllers.HomeController import HomeController
from app.http.controllers.AboutController import AboutController

routes = [
    Get().route('/home', HomeController().show()),
    Get().route('/contact', view('index', { "name": "bill", 'lastname': "Mancuso" })),
    Get().route('/about', AboutController().show())
]