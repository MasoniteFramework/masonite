"""Web Routes."""

from masonite.routes import Get

ROUTES = [Get("/", "WelcomeController@show").name("welcome")]
