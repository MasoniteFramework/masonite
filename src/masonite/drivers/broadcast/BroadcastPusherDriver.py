"""Module for the Pusher websocket driver."""

from masonite.contracts import BroadcastContract
from masonite.drivers import BaseDriver
from masonite.exceptions import DriverLibraryNotFound
from masonite.helpers import config


class BroadcastPusherDriver(BroadcastContract, BaseDriver):
    """Class for the Pusher websocket driver."""

    def __init__(self):
        """Pusher driver constructor.

        Arguments:
            BroadcastConfig {config.broadcast} -- Broadcast configuration.
        """
        self.ssl_message = True

    def ssl(self, boolean):
        """Set whether to send data with SSL enabled.

        Arguments:
            boolean {bool} -- Boolean on whether to set SSL.

        Returns:
            self
        """
        self.ssl_message = boolean
        return self

    def channel(self, channels, message, event='base-event'):
        """Specify which channel(s) you want to send information to.

        Arguments:
            channels {string|list} -- Can be a string for the channel or a list of strings for the channels.
            message {string} -- The message you want to send to the channel(s)

        Keyword Arguments:
            event {string} -- The event you want broadcasted along with your data. (default: {'base-event'})

        Raises:
            DriverLibraryNotFound -- Thrown when pusher is not installed.

        Returns:
            string -- Returns the message sent.
        """
        try:
            import pusher
        except ImportError:
            raise DriverLibraryNotFound(
                'Could not find the "pusher" library. Please pip install this library running "pip install pusher"')

        configuration = config('broadcast.drivers.pusher')

        pusher_client = pusher.Pusher(
            app_id=str(configuration['app_id']),
            key=configuration['client'],
            secret=configuration['secret'],
            ssl=self.ssl_message
        )

        if isinstance(message, str):
            message = {'message': message}

        if isinstance(channels, list):
            for channel in channels:
                pusher_client.trigger(channel, event, message)
        else:
            pusher_client.trigger(channels, event, message)

        return message
