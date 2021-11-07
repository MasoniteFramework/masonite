from src.masonite.authorization import Policy


class PostPolicy(Policy):
    def create(self, user):
        return user.email == "idmann509@gmail.com"

    def view_any(self, user=None):
        """Here we allow guests (non-authenticated) users by declaring the user optional else
        only authenticated users would have been allowed."""
        return True

    def view(self, user, instance):
        return False

    def update(self, user, instance):
        return user.id == instance.user_id

    def delete(self, user, instance):
        if user.id != instance.user_id:
            return self.deny("You do not own this post")
        else:
            return self.allow()

    def force_delete(self, user, instance):
        return False

    def restore(self, user, instance):
        return False
