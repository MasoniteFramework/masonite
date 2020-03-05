"""Module for using the Ably websocket driver."""

from ...contracts import BroadcastContract
from ...drivers import BaseDriver
from ...exceptions import DriverLibraryNotFound
from ...helpers import config


class BroadcastAblyDriver(BroadcastContract, BaseDriver):
    """Class for the Ably Driver."""

    def __init__(self):
        """Ably driver constructor.

        Arguments:
            BroadcastConfig {config.broadcast} -- Broadcast configuration setting.
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
            DriverLibraryNotFound -- Thrown when ably is not installed.

        Returns:
            string -- Returns the message sent.
        """
        try:
            from ably import AblyRest
        except ImportError:
            raise DriverLibraryNotFound(
                'Could not find the "ably" library. Please pip install this library running "pip install ably"')

        configuration = config('broadcast.drivers.ably')
        if not configuration:
            raise Exception('Could not find ably broadcast configuration')

        client = AblyRest('{0}'.format(
            configuration['secret']
        ))

        if isinstance(channels, list):
            for channel in channels:
                ably_channel = client.channels.get(channel)
                ably_channel.publish(event, message)
        else:
            channel = client.channels.get(channels)
            channel.publish(event, message)

        return message
