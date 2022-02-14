from .AuthorizationResponse import AuthorizationResponse


class Policy:
    
    def __init__(self, model):
        self.model = model

    def allow(self, message="", code=None):
        return AuthorizationResponse.allow(message, code)

    def deny(self, message="", code=None):
        return AuthorizationResponse.deny(message, code)
