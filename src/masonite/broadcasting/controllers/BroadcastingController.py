from ..Broadcast import Broadcast
from ...request import Request
from ...controllers import Controller


class BroadcastingController(Controller):
    """Authorization Broadcasting Controller used by broadcasting clients to verify if
    user is authorized to listen to private and presence channels."""

    def authorize(self, request: Request, broadcast: Broadcast):
        return broadcast.driver("pusher").authorize(
            request.input("channel_name"), request.input("socket_id")
        )
