from http.request import Request
from http.routes import Route, Get
from templates.home import Home

routes = [
    Get().route('/home', Home()),
    Get().route('/contact', 'output stuff here too')
]
