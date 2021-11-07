class Cookie:
    def __init__(
        self,
        name,
        value,
        expires=None,
        http_only=True,
        path="/",
        timezone=None,
        secure=False,
    ):
        self.name = name
        self.value = value
        self.http_only = http_only
        self.secure = secure
        self.expires = expires
        self.timezone = timezone
        self.path = path

    def render(self):
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

        return response
