"""New Controller Command."""
from ..view import View
from ..app import App
from ..helpers.filesystem import make_directory

from cleo import Command


class ControllerCommand(Command):
    """
    Creates a controller.

    controller
        {name : Name of the controller you would like to create}
        {--r|--resource : Create a controller as a resource}
        {--e|--exact : For add the name controller without `Controller` text}
    """

    def handle(self):
        controller = self.argument("name")
        view = View(App())

        if not self.option("exact"):
            controller = controller + "Controller"

        if not make_directory("app/http/controllers/{0}.py".format(controller)):
            return self.line_error("{0} Controller Exists!".format(controller))

        with open("app/http/controllers/{0}.py".format(controller), "w+") as f:
            if view.exists("/masonite/snippets/scaffold/controller"):
                if self.option("resource"):
                    template = "/masonite/snippets/scaffold/controller_resource"
                else:
                    template = "/masonite/snippets/scaffold/controller"

                f.write(
                    view.render(
                        template, {"class": controller.split("/")[-1]}
                    ).rendered_template
                )

        self.info("Controller Created Successfully!")
