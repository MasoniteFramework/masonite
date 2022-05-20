from ..facades import View


class ViewController:
    """Controller with one method to render a view with data."""

    def __init__(self, template: str, data: dict):
        self.template = template
        self.data = data

    def show(self) -> "View":
        return View.render(self.template, self.data)
