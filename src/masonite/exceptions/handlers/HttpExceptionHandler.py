class HttpExceptionHandler:
    def __init__(self, application):
        self.application = application

    def handle(self, exception):
        status_code = exception.get_status()
        view_name = f"errors/{status_code}"
        response = self.application.make("response")
        if self.application.make("view").exists(view_name):
            return response.view(
                self.application.make("view").render(
                    f"errors/{status_code}", {"message": exception.get_response()}
                ),
                status_code,
            )
        else:
            return response.view(exception.get_response(), status_code)
