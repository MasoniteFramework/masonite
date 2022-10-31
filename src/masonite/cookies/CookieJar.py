from typing import Any, List, Tuple
import pendulum

from .Cookie import Cookie
from ..utils.time import cookie_expire_time


class CookieJar:
    """Cookie jar used to manage cookies in the request and response."""

    def __init__(self):
        self.cookies: dict = {}
        self.loaded_cookies: dict = {}
        self.deleted_cookies: dict = {}

    def add(self, name: str, value: Any, **options) -> None:
        """Create a cookie and add it to the jar."""
        self.cookies.update({name: Cookie(name, value, **options)})

    def all(self) -> dict:
        """Get all cookies (added manually and loaded from request) from the jar."""
        cookies = self.loaded_cookies
        cookies.update(self.cookies)
        return cookies

    def all_added(self) -> dict:
        """Get all cookies added to the jar."""
        return self.cookies

    def get(self, name: str) -> "Cookie":
        """Get a cookie with the given name."""
        aggregate = self.all()
        return aggregate.get(name)

    def exists(self, name: str) -> bool:
        """Check if the given cookie name exists in the jar."""
        return name in self.cookies or name in self.loaded_cookies

    def is_expired(self, name: str) -> bool:
        """Check if the given cookie name is expired."""
        cookie = self.get(name)
        return cookie.expires < pendulum.now()

    def delete(self, name: str) -> None:
        """Delete a cookie with the given name from the jar. This will remove it from the jar
        and flag it as a cookie to be deleted (by forcing its expiration date)."""
        self.deleted_cookies.update(
            {
                name: Cookie(
                    name, "", expires=cookie_expire_time("expired"), timezone="GMT"
                )
            }
        )
        if name in self.cookies:
            self.cookies.pop(name)

        if name in self.loaded_cookies:
            self.loaded_cookies.pop(name)

    def load_cookie(self, name: str, value: Any) -> None:
        """Load a cookie into the jar with given name and value."""
        self.loaded_cookies.update({name: Cookie(name, value)})

    def to_dict(self) -> dict:
        """Render the jar as a dictionary containing all cookies added manually and loaded cookies."""
        dic = {}
        aggregate = self.cookies
        aggregate.update(self.loaded_cookies)
        for name, cookie in aggregate.items():
            dic.update({name: cookie.value})

        return dic

    def load(self, cookie_string: str) -> "CookieJar":
        """Load a cookie into the jar from a HTTP cookie string."""
        for compound_value in cookie_string.split("; "):
            if "=" in compound_value:
                key, value = compound_value.split("=", 1)
                key, value = key.strip(), value.strip()
                self.load_cookie(key, value)
        return self

    def render_response(self) -> "List[Tuple[str, str]]":
        """Render the cookie jar as list of tuple representing each cookies. This will be used to
        be inserted in the WSGI response.

        [
            ("Set-Cookie", "name=value; Expires=Thu, 31 Oct 2021 07:28:00 GMT;"),
            ("Set-Cookie", "other_name=value2;")
        ]
        """
        cookies = []
        for cookie in {**self.deleted_cookies, **self.all_added()}.values():
            cookies.append(("Set-Cookie", cookie.render()))

        return cookies

    def as_string(self) -> str:
        """Transform back the cookie jar as a string (as found in HTTP_COOKIE header)."""
        cookie_strings = []
        aggregate = self.cookies
        aggregate.update(self.loaded_cookies)
        for name, cookie in aggregate.items():
            cookie_strings.append(f"{name}={cookie.value}")
        return "; ".join(cookie_strings)
