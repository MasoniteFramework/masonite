from .. import Middleware
from ...facades import Session
from ...validation import MessageBag


class ShareErrorsInSessionMiddleware(Middleware):
    """This part verifies if there are any errors stored in Session.
    If there is a validation error then it shares the "errors" key to display the errors in frontend
    else it will return an empty MessageBag object.
    """

    def before(self, request, _):
        request.app.make("request").session = Session

        request.app.make("view").share(
            {
                "errors": MessageBag(Session.pull("errors") or {}),
            }
        )
        return request

    def after(self, request, _):
        return request
