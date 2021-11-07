from src.masonite.routes import Route
from src.masonite.broadcasting import Broadcast
from src.masonite.authentication import Auth

ROUTES = [
    Route.get("/", "WelcomeController@show").name("welcome"),
    Route.get("/flash_data", "WelcomeController@flash_data"),
    Route.get("/sessions", "WelcomeController@play_with_session").name(
        "play_with_session"
    ),
    Route.post("/", "WelcomeController@show"),
    Route.post("/input", "WelcomeController@input"),
    Route.post("/upload", "WelcomeController@upload").name("upload"),
    Route.get("/test", "WelcomeController@test"),
    Route.get("/emit", "WelcomeController@emit"),
    Route.get("/view", "WelcomeController@view"),
    Route.get("/mail", "MailableController@view"),
    Route.get("/users/@id", "WelcomeController@test").name("users.profile"),
]

Broadcast.routes()
Auth.routes()
