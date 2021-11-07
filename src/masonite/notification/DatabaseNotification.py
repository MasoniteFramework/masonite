"""DatabaseNotification Model."""
import pendulum
from masoniteorm.relationships import morph_to
from masoniteorm.models import Model


class DatabaseNotification(Model):
    """DatabaseNotification Model allowing notifications to be stored in database."""

    __fillable__ = ["id", "type", "data", "read_at", "notifiable_id", "notifiable_type"]
    __table__ = "notifications"

    @morph_to("notifiable_type", "notifiable_id")
    def notifiable(self):
        """Get the notifiable entity that the notification belongs to."""
        return

    def mark_as_read(self):
        """Mark the notification as read."""
        if not self.read_at:
            self.read_at = pendulum.now()
            return self.save(query=True)

    def mark_as_unread(self):
        """Mark the notification as unread."""
        if self.read_at:
            self.read_at = None
            return self.save(query=True)

    @property
    def is_read(self):
        """Determine if a notification has been read."""
        return self.read_at is not None

    @property
    def is_unread(self):
        """Determine if a notification has not been read yet."""
        return self.read_at is None
