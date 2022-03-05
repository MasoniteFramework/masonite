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

        """This part verifies if there are any validation_errors stored in Session.
        If there is a validation error then it shares the "errors" key to display the errors in frontend
        else it will return an empty MessageBag object.
        """
        if Session.get("validation_errors"):
            request.app.make("view").share(
                {
                    "errors": MessageBag(Session.pull("validation_errors")),
                }
            )
        else:
            request.app.make("view").reset_vaidation_errors()

        return request

    def after(self, request, _):
        Session.save()
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

        Session.set("validation_errors", errors)

        return Response

    def with_success(self, success):
        if isinstance(success, list):
            Session.flash("success", {"success": success})
        else:
            Session.flash("success", success)

        return Response
