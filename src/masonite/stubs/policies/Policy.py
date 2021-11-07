from masonite.authorization import Policy


class __class__(Policy):
    def view_admin(self, user):
        return False
