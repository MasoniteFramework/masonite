from app.http.providers.routes import Api
from app.Users import Users

routes = [
    Api().model(Users),
]