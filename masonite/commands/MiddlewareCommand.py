""" New Middleware Command """
import os

from masonite.view import View
from masonite.app import App
from masonite.helpers.filesystem import make_directory

from cleo import Command


class MiddlewareCommand(Command):
    """
    Creates a middleware

    middleware
        {name : Name of the middleware}
    """

    def handle(self):
        middleware = "{}".format(self.argument('name'))
        view = View(App())

        if not make_directory('app/http/middleware/{}{}.py'.format(middleware, 'Middleware')):
            return self.error('{} Middleware Exists!'.format(middleware))

        f = open('app/http/middleware/{}{}.py'.format(middleware, 'Middleware'), 'w+')
        if view.exists('/masonite/snippets/scaffold/middleware'):
            template = '/masonite/snippets/scaffold/middleware'

            f.write(
                view.render(
                    template, {'class': middleware}).rendered_template
            )

            self.info('Middleware Created Successfully!')
            return f.close()
