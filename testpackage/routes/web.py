"""Test Package Routes."""
from src.masonite.routes import Get


ROUTES = [
    Get("/package-route", "TestController@testing"),
]