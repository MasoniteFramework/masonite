from masonite.contracts.BroadcastContract import BroadcastContract
from masonite.exceptions import DriverLibraryNotFound
from masonite.drivers.BaseDriver import BaseDriver


class BroadcastAblyDriver(BroadcastContract, BaseDriver):

    def __init__(self, BroadcastConfig):
        self.config = BroadcastConfig
        self.ssl_message = True

    def ssl(self, boolean):
        self.ssl_message = boolean
        return self

    def channel(self, channels, message, event='base-event'):
        try:
            from ably import AblyRest
        except ImportError:
            raise DriverLibraryNotFound(
                'Could not find the "ably" library. Please pip install this library running "pip install ably"')

        client = AblyRest('{0}'.format(
            self.config.DRIVERS['ably']['secret']
        ))

        if isinstance(channels, list):
            for channel in channels:
                ably_channel = client.channels.get(channel)
                ably_channel.publish(event, message)
        else:
            channel = client.channels.get(channels)
            channel.publish(event, message)

        return message
