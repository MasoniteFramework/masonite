class HttpExceptionHandler:
    def __init__(self, application):
        self.application = application

    def handle(self, exception):
        status_code = exception.get_status()
        view_name = f"errors/{status_code}"
        response = self.application.make("response")
        request = self.application.make("request")

        if request.accepts_json():
            payload = {
                "status": exception.get_status(),
                "message": exception.get_response(),
            }
            return response.json(payload, status_code)

        # Renders HTTP exception as HTML with predefined error page if exists
        if self.application.make("view").exists(view_name):
            return response.view(
                self.application.make("view").render(
                    f"errors/{status_code}", {"message": exception.get_response()}
                ),
                status_code,
            )
        else:
            # Else render the exception without using template
            return response.view(exception.get_response(), status_code)
