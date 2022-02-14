from masonite.authorization import Policy


class __class__(Policy):
    def __init__(self, model):
        self.model = model

    def create(self, user):
        return False

    def view_any(self, user):
        return False

    def view(self, user, instance):
        return False

    def update(self, user, instance):
        return False

    def delete(self, user, instance):
        return False

    def force_delete(self, user, instance):
        return False

    def restore(self, user, instance):
        return False
