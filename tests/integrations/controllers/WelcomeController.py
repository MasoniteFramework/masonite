from src.masonite.controllers import Controller
from src.masonite.views import View
from src.masonite.response.response import Response
from src.masonite.request import Request
from src.masonite.filesystem import Storage
from src.masonite.broadcasting import Broadcast, Channel
from src.masonite.facades import Session, Config, Gate


class CanBroadcast:
    def broadcast_on(self):
        return Channel(f"private-shipped")

    def broadcast_with(self):
        return vars(self)

    def broadcast_as(self):
        return self.__class__.__name__


class OrderProcessed(CanBroadcast):
    def __init__(self):
        self.order_id = 1


class WelcomeController(Controller):
    def play_with_session(self, request: Request, view: View):
        # Session.flash("test", "hello flashed")
        # Session.set("test_persisted", "hello persisted in session")
        # request.app.make("session").set("test_persisted", "hello persisted")
        return view.render("welcome")

    def show(self, request: Request, view: View):
        request.app.make("session").flash("test", "value")
        return view.render("welcome")

    def flash_data(self, request: Request, response: Response, view: View):
        request.app.make("session").flash("test", "value")
        return response.with_input().redirect("/sessions")

    def form_with_input(self, request: Request, response: Response, view: View):
        return response.redirect("/sessions").with_input()

    def test(self):
        return "test"

    def api(self):
        return {"key": "value"}

    def emit(self, broadcast: Broadcast):
        broadcast.channel("private-orders", OrderProcessed())
        return "emitted"

    def view(self, view: View):
        return view.render("welcome")

    def upload(self, request: Request, storage: Storage):
        return storage.disk("s3").store(request.input("profile"))

    def create(self):
        return "user created", 201

    def not_found(self):
        return "not found", 404

    def unauthorized(self):
        return "unauthorized", 401

    def input(self, request: Request):
        return request.all()
        return "input"

    def forbidden(self):
        return "forbidden", 403

    def empty(self):
        return "", 204

    def redirect_url(self, response: Response):
        return response.redirect("/")

    def redirect_route(self, response: Response):
        return response.redirect(name="test")

    def redirect_route_params(self, response: Response):
        return response.redirect(name="test_params", params={"id": 1})

    def response_with_headers(self, response: Response):
        response.header("TEST", "value")
        response.header("TEST2", "value2")
        return ""

    def view_with_context(self, view: View):
        return view.render(
            "welcome",
            {"count": 1, "users": ["John", "Joe"], "other_key": {"nested": 1}},
        )

    def json(self, response: Response):
        return response.json(
            {
                "key": "value",
                "key2": [1, 2],
                "other_key": {
                    "nested": 1,
                    "nested_again": {"a": 1, "b": 2},
                },
            }
        )

    def session(self, request: Request):
        request.app.make("session").flash("key", "value")
        return "session"

    def session_with_errors(self, request: Request, response: Response):
        request.app.make("session").flash("key", "value")
        request.app.make("session").flash(
            "errors",
            {"email": "Email required", "password": "Password too short", "name": ""},
        )
        return "session"

    def with_errors(self, response: Response):
        return response.back().with_errors(
            {"email": "Email required", "password": "Password too short", "name": ""}
        )

    def session2(self, request: Request):
        request.app.make("session").flash(
            "key", {"nested": 1, "nested_again": {"key2": "value2"}}
        )
        return "session2"

    def with_params(self):
        return ""

    def auth(self, request: Request):
        request.app.make("auth").guard("web").attempt("idmann509@gmail.com", "secret")
        return "logged in"

    def not_authorized(self):
        # if current user not authorized it will raise an exception
        Gate.authorize("display-admin")

    def use_authorization_helper(self, request: Request):
        request.authorize("display-admin")

    def authorizations(self, view: View):
        return view.render("authorizations")
