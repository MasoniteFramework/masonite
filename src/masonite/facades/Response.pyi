from typing import Any

class Response:
    """Response facade."""

    def json(payload: Any, status: int = 200) -> bytes:
        """Set the response as a JSON response."""
        ...
    def make_headers(content_type: str = "text/html; charset=utf-8") -> None:
        """Recompute Content-Length of the response after modyifing it."""
        ...
    def header(name: str, value: str = None) -> "None|str":
        """Get response header for the given name if no value provided or add headers to response."""
        ...
    def get_headers(self) -> list:
        """Get all response headers."""
        ...
    def cookie(name: str, value: str = None, **options) -> "None|str":
        """Get response cookie for the given name if no value provided or add cookie to
        the response with the given name, value and options."""
        ...
    def delete_cookie(name: str) -> "Response":
        """Delete the cookie with the given name from the response."""
        ...
    def get_response_content(self) -> bytes:
        """Get response content."""
        ...
    def status(status: "str|int") -> "Response":
        """Set HTTP status code of the response."""
        ...
    def is_status(code: int) -> bool:
        """Check if response has the given status code."""
        ...
    def get_status_code(self) -> str:
        """Gets the HTTP status code of the response as a human string, like "200 OK"."""
        ...
    def get_status(self): ...
    def data(self) -> bytes:
        """Get the response content as bytes."""
        ...
    def converted_data(self) -> "str|bytes":
        """Get the response content as string or bytes so that the WSGI server handles it."""
        ...
    def view(view: Any, status: int = 200) -> "bytes|Response":
        """Set the response as a string or view."""
        ...
    def back(self) -> "Response":
        """Set the response as a redirect response back to previous path defined from the
        request."""
        ...
    def redirect(
        location: str = None,
        name: str = None,
        params: dict = {},
        url: str = None,
        status: int = 302,
    ) -> "Response":
        """Set the response as a redirect response. The redirection location can be defined
        with the location URL or with a route name. If a route name is used, route params can
        be provided."""

        ...
    def to_bytes(self) -> "bytes":
        """Converts the response to bytes."""
        ...
    def download(name: str, location: str, force: bool = False) -> "Response":
        """Set the response as a file download response."""
        ...
