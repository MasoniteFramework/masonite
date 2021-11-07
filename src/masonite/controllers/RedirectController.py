from ..response import Response


class RedirectController:
    def __init__(self, url, status):
        self.url = url
        self.status = status

    def redirect(self, response: Response):
        return response.redirect(self.url, status=self.status)
