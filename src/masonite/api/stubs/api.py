"""API Config"""
from masonite.environment import env

from app.models.User import User

DRIVERS = {
    "jwt": {
        "algorithm": "HS512",
        "secret": env("JWT_SECRET"),
        "model": User,
        "expires": None,
        "authenticates": False,
        "version": None,
    }
}
