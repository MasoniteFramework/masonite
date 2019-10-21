"""A View Service Provider."""

from jinja2 import FileSystemLoader

from ..provider import ServiceProvider
from ..view import View


class ViewProvider(ServiceProvider):

    wsgi = False

    def register(self):
        view = View(self.app)
        self.app.bind('ViewClass', view)
        self.app.bind('View', view.render)

    def boot(self, view: View):
        view.add_environment('src/masonite/snippets', loader=FileSystemLoader)
        self.publishes_migrations([
            'storage/append_from.txt'
        ])
