from ..response import Response


class RedirectController:
    """Controller with one method to create a redirection."""

    def __init__(self, url: str, status: int):
        self.url = url
        self.status = status

    def redirect(self, response: Response) -> "Response":
        return response.redirect(self.url, status=self.status)
