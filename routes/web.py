from app.http.providers.routes import Get
from resources.views.home import Home
from app.http.providers.view import view

routes = [
    Get().route('/home', Home()),
    Get().route('/contact', view('index', { "name": "bill", 'lastname': "Mancuso" }))
]