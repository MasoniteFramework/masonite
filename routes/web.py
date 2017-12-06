from http.routes import Get
from resources.views.home import Home
from http.view import view

routes = [
    Get().route('/home', Home()),
    Get().route('/contact', view('index', { "name": "bill", 'lastname': "Mancuso" }))
]