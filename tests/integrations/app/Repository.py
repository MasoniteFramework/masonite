from .User import User


class Repository:
    def __init__(self, user: User):
        self.user = user
