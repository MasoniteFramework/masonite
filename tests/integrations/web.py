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
    Route.get("/contact", "WelcomeController@contact"),
    Route.post("/contact", "WelcomeController@contact_post"),
    Route.post("/input", "WelcomeController@input"),
    Route.post("/upload", "WelcomeController@upload").name("upload"),
    Route.get("/test", "WelcomeController@test"),
    Route.get("/emit", "WelcomeController@emit"),
    Route.get("/view", "WelcomeController@view"),
    Route.get("/mail", "MailableController@view"),
    Route.get("/users/@id", "WelcomeController@show_user").name("users.profile"),
    Route.view("/test_view", "test_view", {"show": "111"}),
    Route.get("/api/uploads/", "WelcomeController@test").middleware("throttle:api"),
]

Broadcast.routes()
Auth.routes()
