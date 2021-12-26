from src.masonite.routes import Route


ROUTES = [
    Route.get("/try", "WelcomeController@show").name("api.try"),
]
