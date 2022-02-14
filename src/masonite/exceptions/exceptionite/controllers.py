from ...request import Request
from ...controllers import Controller
from ...response import Response


class ExceptioniteController(Controller):
    def run_action(self, request: Request, response: Response):
        handler = request.app.make("exception_handler").get_driver("exceptionite")
        data = handler.run_action(request.input("action_id"), request.input("options"))
        try:
            return response.json({"message": "ok", "data": data}, 200)
        except:  # noqa: E722
            return response.json({"message": "An error happened", "data": data}, 400)
