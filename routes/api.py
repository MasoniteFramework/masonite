''' API Routes '''
from masonite.routes import Api
from app.User import User

ROUTES = [
    Api().model(User).exclude(['password', 'token']),
]
