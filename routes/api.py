''' API Routes '''
from masonite.routes import Api
from app.Users import Users

ROUTES = [
    # Api().model(Users).exclude(['password', 'token']),
]
