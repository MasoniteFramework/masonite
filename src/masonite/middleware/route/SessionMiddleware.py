from .. import Middleware
from ...utils.str import random_string
from ...facades import Request, Session, Response
from ...validation import MessageBag


class SessionMiddleware(Middleware):
    def before(self, request, response):
        if not request.cookie("SESSID"):
            session_code = random_string(10)
            response.cookie("SESSID", session_code)
            request.cookie("SESSID", session_code)
        Session.start()
        request.app.make("response").with_input = self.with_input
        request.app.make("response").with_errors = self.with_errors
        request.app.make("response").with_success = self.with_success
        request.app.make("request").session = Session

        # TODO: Check this in Masonite 5
        # errors are stored in session flash so 'getting' them
        # actually clears them out of the session
        errors = Session.get("errors")
        request.app.make("view").share({"errors": MessageBag(errors or {}).helper})
        # TODO: remove this in Masonite 5
        request.app.make("view").share({"bag": MessageBag(errors or {}).helper})
        # if any errors then re-add them to the session
        if errors:
            Session.flash("errors", errors)

        return request

    def after(self, request, _):
        return request

    def with_input(self):
        for key, value in Request.all().items():
            Session.flash(key, value)
        return Response

    def with_errors(self, errors):
        if isinstance(errors, list):
            Session.flash("errors", {"errors": errors})
        else:
            Session.flash("errors", errors)

        return Response

    def with_success(self, success):
        if isinstance(success, list):
            Session.flash("success", {"success": success})
        else:
            Session.flash("success", success)

        return Response
