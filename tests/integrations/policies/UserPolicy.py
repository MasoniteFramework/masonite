from src.masonite.authorization import Policy


class UserPolicy(Policy):
    def view(self, user):
        return True
