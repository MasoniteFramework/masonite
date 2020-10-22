class Cookie:
    def __init__(
        self, name, value, expires=None, http_only=True, path=None, timezone=None
    ):
        self.name = name
        self.value = value
        self.http_only = http_only
        self.expires = expires
        self.timezone = timezone
        self.path = path

    def render(self):
        response = f"{self.name}={self.value};"
        if self.http_only:
            response += "HttpOnly;"
        if self.expires:
            if self.timezone:
                response += f"{self.expires} {self.timezone};"
            else:
                response += f"{self.expires};"
        if self.path:
            response += f"Path={self.path};"

        return response
