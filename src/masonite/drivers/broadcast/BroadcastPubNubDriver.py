"""Module for the PubNub websocket driver."""

from ...contracts import BroadcastContract
from ...drivers import BaseDriver
from ...exceptions import DriverLibraryNotFound
from ...helpers import config


class BroadcastPubNubDriver(BroadcastContract, BaseDriver):
    """Class for the PubNub websocket driver."""

    def __init__(self):
        """PubNub driver constructor.

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

    def channel(self, channels, message, event="base-event"):
        """Specify which channel(s) you want to send information to.

        Arguments:
            channels {string|list} -- Can be a string for the channel or a list of strings for the channels.
            message {string} -- The message you want to send to the channel(s)

        Keyword Arguments:
            event {string} -- The event you want broadcasted along with your data. (default: {'base-event'})

        Raises:
            DriverLibraryNotFound -- Thrown when pubnub is not installed.

        Returns:
            string -- Returns the message sent.
        """
        try:
            from pubnub.pnconfiguration import PNConfiguration
            from pubnub.pubnub import PubNub
        except ImportError:
            raise DriverLibraryNotFound(
                'Could not find the "pubnub" library. Please pip install this library running "pip install pubnub"'
            )

        configuration = config("broadcast.drivers.pubnub")
        pnconfig = PNConfiguration()
        pnconfig.publish_key = configuration["publish_key"]
        pnconfig.subscribe_key = configuration["subscribe_key"]
        pnconfig.secret = configuration["secret"]
        pnconfig.ssl = self.ssl_message
        pnconfig.uuid = config("application.name")

        pubnub = PubNub(pnconfig)

        if isinstance(message, str):
            message = {"message": message}

        if isinstance(channels, str):
            channels = [channels]

        for channel in channels:
            envelope = pubnub.publish().channel(channel).message(message).sync()
            if envelope.status.is_error():
                print(
                    "PubNub Broadcast: error sending message to channel {0}.".format(
                        channel
                    )
                )
        return message
