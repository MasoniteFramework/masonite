from typing import TYPE_CHECKING, List, Any

if TYPE_CHECKING:
    from ..routes import Route

class Request:
    """Request facade."""

    def load():
        """Load request from environment."""
        ...
    def load_params(params: dict = None):
        """Load request parameters."""
        ...
    def param(param: str, default: str = "") -> str:
        """Get query string parameter from request."""
        ...
    def get_route() -> "Route":
        """Get Route associated to request if any."""
        ...
    def get_path() -> str:
        """Get request path (read from PATH_INFO) environment variable without eventual query
        string parameters."""
        ...
    def get_path_with_query() -> str:
        """Get request path (read from PATH_INFO) environment variable with eventual query
        string parameters."""
        ...
    def get_back_path() -> str:
        """Get previous request path if it has been defined as '__back' input."""
        ...
    def get_request_method() -> str:
        """Get request method (read from REQUEST_METHOD environment variable)."""
        ...
    def input(name: str, default: str = "") -> str:
        """Get a specific request input value with the given name. If the value does not exist in
        the request return the default value."""
        ...
    def cookie(name: str, value: str = None, **options) -> None:
        """If no value provided, read the cookie value with the given name from the request. Else
        create a cookie in the request with the given name and value.
        Some options can be passed when creating cookie, refer to CookieJar class."""
        ...
    def delete_cookie(name: str) -> "Request":
        """Delete cookie with the given name from the request."""
        ...
    def header(name: str, value: str = None) -> "str|None":
        """If no value provided, read the header value with the given name from the request. Else
        add a header in the request with the given name and value."""
        ...
    def all() -> dict:
        """Get all inputs from the request as a dictionary."""
        ...
    def only(*inputs: List[str]) -> dict:
        """Get only the given inputs from the request as a dictionary."""
        ...
    def old(key: str):
        """Get value from session for the given key."""
        ...
    def is_not_safe() -> bool:
        """Check if the current request is considered 'safe', meaning that the request method is
        GET, OPTIONS or HEAD."""
        ...
    def user() -> "None|Any":
        """Get the current authenticated user if any. LoadUserMiddleware needs to be used for user
        to be populated in request."""
        ...
    def set_user(user: Any) -> "Request":
        """Set the current authenticated user of the request."""
        ...
    def remove_user() -> "Request":
        """Log out user of the current request."""
        ...
    def contains(route: str) -> bool:
        """Check if current request path match the given URL."""
        ...
    def get_subdomain(exclude_www: bool = True) -> "None|str":
        """Get the request subdomain if subdomains are enabled."""
        ...
    def get_host() -> str:
        """Get the request host (from HTTP_HOST environment variable)."""
        ...
    def activate_subdomains():
        """Enable subdomains for this request."""
        ...
    def is_ajax() -> bool:
        """Check if the current request is an AJAX request."""
        ...
