import pendulum
import uuid
from typing import TYPE_CHECKING, Any, List, Tuple

from ..routes import Route

if TYPE_CHECKING:
    from ..foundation import Application


class Auth:
    def __init__(self, application: "Application", guard_config: dict = {}):
        self.application = application
        self.guards: dict = {}
        self._guard = None
        self.guard_config: dict = guard_config or {}
        self.options: dict = {}
        self._user = None

    def add_guard(self, name: str, guard: "Any") -> None:
        """Register a new authentication guard."""
        self.guards.update({name: guard})

    def set_configuration(self, config: dict) -> "Auth":
        self.guard_config = config
        return self

    def guard(self, guard: "Any") -> "Auth":
        """Set the current authentication guard to use."""
        self._guard = guard
        return self

    def get_guard(self, name: str = None) -> "Any":
        """Get the default authentication guard or the guard with given name."""
        if name is None and self._guard is None:
            return self.guards[self.guard_config.get("default")]

        return self.guards[self._guard]

    def get_config_options(self, guard: str = None) -> dict:
        if guard is None:
            options = self.guard_config.get(self.guard_config.get("default"), {})
            options.update(self.options)
            return options

        options = self.guard_config.get(guard, {})
        options.update(self.options)
        return options

    def attempt(self, email: str, password: str, once: bool = False):
        """Attempt to authenticate the user with the given email/password."""
        auth_config = self.get_config_options()
        auth_config.update({"once": once})
        user = self.get_guard().set_options(auth_config).attempt(email, password)
        self.set_user(user)
        return user

    def attempt_by_id(self, user_id: "str|int", once: bool = False):
        """Attempt to authenticate the user with the given user ID."""
        auth_config = self.get_config_options()
        auth_config.update({"once": once})
        user = self.get_guard().set_options(auth_config).attempt_by_id(user_id)
        self.set_user(user)
        return user

    def logout(self) -> None:
        """Logout the current authenticated user."""
        self.application.make("request").remove_user()
        self.application.make("response").delete_cookie("token")
        self.get_guard().set_options(self.get_config_options()).logout()
        self._user = None

    def user(self) -> "Any":
        """Get the current authenticated user."""
        if self._user:
            return self._user
        return self.get_guard().set_options(self.get_config_options()).user()

    def register(self, dictionary: dict) -> "Any":
        """Register a new user with given data."""
        auth_config = self.get_config_options()
        return self.get_guard().set_options(auth_config).register(dictionary)

    def set_user(self, user: "Any") -> "Auth":
        """Set the current authenticated user."""
        self._user = user
        return self

    def password_reset(self, email: str) -> "Tuple[None, None]|Tuple[int,str]":
        """Reset password of the user with the given email."""
        token = str(uuid.uuid4())
        auth_config = self.get_config_options()
        auth = self.get_guard().set_options(auth_config).get_auth_column(email)
        if not auth:
            return (None, None)
        try:
            existing = (
                self.application.make("builder")
                .new()
                .table(self.guard_config.get("password_reset_table"))
                .where("email", email)
                .first()
            )
            if existing:
                token = existing["token"]
            else:
                self.application.make("builder").new().table(
                    self.guard_config.get("password_reset_table")
                ).create(
                    {
                        "email": email,
                        "token": token,
                        "expires_at": pendulum.now()
                        .add(minutes=self.guard_config.get("password_reset_expiration"))
                        .to_datetime_string()
                        if self.guard_config.get("password_reset_expiration")
                        else None,
                        "created_at": pendulum.now().to_datetime_string(),
                    }
                )
        except Exception:
            return (None, None)

        self.application.make("event").fire("auth.password_reset", email, token)
        return auth, token

    def reset_password(self, password: str, token: str) -> bool:
        """Reset password of the user with the given authentication token."""
        reset_record = (
            self.application.make("builder")
            .new()
            .table(self.guard_config.get("password_reset_table"))
            .where("token", token)
            .first()
        )

        auth_config = self.get_config_options()
        (
            self.get_guard()
            .set_options(auth_config)
            .reset_password(reset_record.get("email"), password)
        )

        (
            self.application.make("builder")
            .new()
            .table(self.guard_config.get("password_reset_table"))
            .where("token", token)
            .delete()
        )

        return True

    @classmethod
    def routes(self) -> "List[Route]":
        """Get the basic authentication routes."""
        return [
            Route.get("/login", "auth.LoginController@show").name("login"),
            Route.get("/logout", "auth.LoginController@logout").name("logout"),
            Route.get("/home", "auth.HomeController@show")
            .name("auth.home")
            .middleware("auth"),
            Route.get("/register", "auth.RegisterController@show").name("register"),
            Route.post("/register", "auth.RegisterController@store").name(
                "register.store"
            ),
            Route.get("/password_reset", "auth.PasswordResetController@show").name(
                "password_reset"
            ),
            Route.post("/password_reset", "auth.PasswordResetController@store").name(
                "password_reset.store"
            ),
            Route.get(
                "/change_password/@token",
                "auth.PasswordResetController@change_password",
            ).name("change_password"),
            Route.post(
                "/change_password/@token",
                "auth.PasswordResetController@store_changed_password",
            ).name("change_password.store"),
            Route.post("/login", "auth.LoginController@store").name("login.store"),
        ]
