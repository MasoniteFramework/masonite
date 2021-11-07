from ..Broadcast import Broadcast
from ...request import Request
from ...controllers import Controller


class BroadcastingController(Controller):
    def authorize(self, request: Request, broadcast: Broadcast):
        return broadcast.driver("pusher").authorize(
            request.input("channel_name"), request.input("socket_id")
        )
