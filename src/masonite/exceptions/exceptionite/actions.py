from exceptionite.actions import Action
from masonite.utils.structures import data as data_dot
import requests


class MasoniteDebugAction(Action):
    name = "Share with Masonite Support"
    icon = "SupportIcon"
    id = "masonite-debug"
    component = "MasoniteSupport"

    def run(self, options={}):
        api_url = "http://localhost:8001/api/tickets/"
        options = data_dot(options)
        all_data = self.handler.get_last_exception_data()
        # token = self.handler.app.make("request").cookie("SESSID")
        data = {}
        if options.get("options.exception.show", False):
            data.update(
                {
                    "exception": all_data.get("exception").get("type"),
                    "message": all_data.get("exception").get("message"),
                }
            )
        if options.get("options.stacktrace.show", False):
            data.update({"stack": all_data.get("exception").get("stacktrace")})
        response = requests.post(
            api_url,
            json=data,
            headers={
                "Content-type": "application/json",
                "Accept": "application/json",
                # "X-CSRF-TOKEN": token,
            },
        )
        if response.status_code == 201:
            return response.json()
        else:
            return {"message": "An error happened"}
