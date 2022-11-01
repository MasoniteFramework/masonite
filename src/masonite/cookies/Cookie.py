from typing import Any


class Cookie:
    """Class used to represent a HTTP cookie."""

    def __init__(
        self,
        name: str,
        value: Any,
        expires=None,
        http_only: bool = True,
        path: str = "/",
        timezone: str = None,
        secure: bool = False,
        samesite: str = "Strict",
    ):
        self.name = name
        self.value = value
        self.http_only = http_only
        self.secure = secure
        self.expires = expires
        self.timezone = timezone
        self.samesite = samesite
        self.path = path

    def render(self) -> str:
        """Render the cookie as a string used in the HTTP response."""
        response = f"{self.name}={self.value};"
        if self.http_only:
            response += "HttpOnly;"
        if self.secure:
            response += "Secure;"
        if self.expires:
            if self.timezone:
                response += f"Expires={self.expires} {self.timezone};"
            else:
                response += f"Expires={self.expires};"
        if self.path:
            response += f"Path={self.path};"
        if self.samesite:
            response += f"SameSite={self.samesite};"

        return response
