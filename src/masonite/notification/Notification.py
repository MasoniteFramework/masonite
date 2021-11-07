"""Base Notification facade."""


class Notification:
    def via(self, notifiable):
        """Defines the notification's delivery channels."""
        raise NotImplementedError("via() method should be implemented.")

    def should_send(self):
        return True

    def ignore_errors(self):
        return False

    def broadcast_on(self):
        return "broadcast"

    @classmethod
    def type(cls):
        """Get notification type defined with class name."""
        return cls.__name__

    def dry(self):
        """Sets whether the notification should be sent or not.

        Returns:
            self
        """
        self._dry = True
        return self

    def fail_silently(self):
        """Sets whether the notification can fail silently (without raising exceptions).

        Returns:
            self
        """
        self._fail_silently = True
        return self
