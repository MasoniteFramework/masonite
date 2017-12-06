from app.http.providers.routes import Get
from resources.views.home import Home
from app.http.providers.view import view
from app.http.controllers.HomeController import HomeController
from app.http.controllers.AboutController import AboutController
from app.http.controllers.ContactController import ContactController

routes = [
    Get().route('/home', HomeController().show()),
    Get().route('/about', AboutController().show()),
    Get().route('/contact', ContactController().show())
]