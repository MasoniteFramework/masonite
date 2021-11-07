class BaseDriver:
    def send(self, notifiable, notification):
        """Implements sending the notification to notifiables through
        this driver."""
        raise NotImplementedError(
            "send() method must be implemented for a notification driver."
        )

    def get_data(self, driver, notifiable, notification):
        """Get the data for the notification."""
        method_name = f"to_{driver}"
        try:
            method = getattr(notification, method_name)
        except AttributeError:
            raise NotImplementedError(
                f"Notification model should implement {method_name}() method."
            )
        else:
            return method(notifiable)
