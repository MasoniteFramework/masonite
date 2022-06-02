from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ...routes import Route

class Api:
    def set_configuration(config: dict) -> "Api": ...
    def generate_token(self) -> str:
        """Generate a JWT token according to JWT api configuration."""
        ...
    def get_token(self) -> str:
        """Get token from request."""
        ...
    def validate_token(token: str) -> bool:
        """Check if given token is valid."""
        ...
    def regenerate_token(token: str) -> str:
        """Re-generate a token based on the given token."""
        ...
    def attempt_by_token(token: str): ...
    @classmethod
    def routes(
        cls, auth_route: str = "/api/auth", reauth_route: str = "/api/reauth"
    ) -> "List[Route]":
        """Get api standard authentication routes."""
        ...
