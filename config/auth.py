''' Where authentication settings should be'''
from app.Users import Users

AUTH = {
    'model': Users,
    'driver': 'cookie'
}
