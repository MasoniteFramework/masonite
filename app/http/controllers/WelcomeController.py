"""Welcome The User To Masonite."""

from src.masonite.view import View
from src.masonite.controllers import Controller
from app.jobs.TestJob import TestJob
from src.masonite import Queue


class WelcomeController(Controller):
    """Controller For Welcoming The User."""

    def show(self, view: View, queue: Queue):
        """Show the welcome page.

        Arguments:
            view {masonite.view.View} -- The Masonite view class.
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.view.View -- The Masonite view class.
        """
        queue.push(TestJob)
        return view.render('welcome')
