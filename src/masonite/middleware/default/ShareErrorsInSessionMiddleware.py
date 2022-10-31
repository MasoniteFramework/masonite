from .. import Middleware
from ...facades import Session
from ...validation import MessageBag


class ShareErrorsInSessionMiddleware(Middleware):
    """Share errors as a Message bag if there are any errors flashed to session. If not the message
    bag will be empty."""

    def before(self, request, _):
        request.app.make("view").share(
            {
                "errors": MessageBag(Session.pull("errors") or {}),
            }
        )
        return request

    def after(self, request, _):
        return request
