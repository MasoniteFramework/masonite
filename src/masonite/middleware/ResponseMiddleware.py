from ..app import App
from ..request import Request
from ..response import Response


class ResponseMiddleware:
    def __init__(self, request: Request, app: App, response: Response):
        self.request = request
        self.app = app
        self.response = response

    def after(self):
        if self.request.redirect_url:
            self.response.redirect(self.request.redirect_url, status=302)
            self.request.reset_redirections()

        if self.app.has("Session") and self.response.is_status(200):
            try:
                self.app.make("Session").driver("memory").reset(flash_only=True)
            except Exception:
                pass
