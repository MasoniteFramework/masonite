"""Exception Handler Module.

A module for controlling exceptions handling when an error occurs doing executing
code in a Masonite application. These errors could are thrown during runtime.
"""

import inspect
import os
import sys
import traceback

from exceptionite.errors import (Handler, SolutionsIntegration,
                                 StackOverflowIntegration)

from .app import App
from .exceptions import DumpException
from .helpers import config
from .listeners import BaseExceptionListener
from .request import Request
from .response import Response
from .view import View

package_directory = os.path.dirname(os.path.realpath(__file__))


class ExceptionHandler:
    """Class for handling exceptions thrown during runtime."""

    def __init__(self, app):
        """ExceptionHandler constructor. Also responsible for loading static files into the container.

        Arguments:
            app {masonite.app.App} -- Container object
        """
        self._app = app
        self.response = self._app.make(Response)

        self._register_static_files()

    def _register_static_files(self):
        """Register static files into the container."""
        storage = config('storage')
        if storage:
            storage.STATICFILES.update(
                {
                    os.path.join(package_directory, 'snippets/exceptions'):
                    '_exceptions/'
                }
            )

    def load_exception(self, exception):
        """Load the exception thrown into this handler.

        Arguments:
            exception {Exception} -- This is the exception object thrown at runtime.
        """
        self._exception = exception

        if self._app.has('Exception{}Handler'.format(exception.__class__.__name__)):

            return self._app.make('Exception{}Handler'.format(exception.__class__.__name__)).handle(exception)

        self.handle(exception)

    def run_listeners(self, exception, stacktraceback):
        for exception_class in self._app.collect(BaseExceptionListener):
            if '*' in exception_class.listens or exception.__class__ in exception_class.listens:
                file, line = self.get_file_and_line(stacktraceback)
                self._app.resolve(exception_class).handle(exception, file, line)

    def get_file_and_line(self, stacktraceback):
        for stack in stacktraceback[::-1]:
            if 'site-packages' not in stack[0]:
                return (stack[0], stack[1])

    def handle(self, exception):
        """Render an exception view if the DEBUG configuration is True. Else this should not return anything.

        Returns:
            None
        """

        stacktraceback = traceback.extract_tb(sys.exc_info()[2])
        self.run_listeners(exception, stacktraceback)
        # Run Any Framework Exception Hooks
        self._app.make('HookHandler').fire('*ExceptionHook')

        # Check if DEBUG is False
        from config import application
        if not application.DEBUG:
            request = self._app.make('Request')
            request.status(500)
            return

        response = self._app.make(Response)

        handler = Handler(exception)
        handler.integrate(
            SolutionsIntegration()
        )
        handler.integrate(
            StackOverflowIntegration(),
        )
        response.view(handler.render(), status=500)


class DD:

    def __init__(self, container):
        self.app = container

    def dump(self, *args):
        dump_list = []
        for i, obj in enumerate(args):
            dump_name = 'ObjDump{}'.format(i)
            self.app.bind(dump_name, obj)
            dump_list.append(dump_name)
        self.app.bind('ObjDumpList', dump_list)
        raise DumpException


class DumpHandler:

    def __init__(self, view: View, request: Request, app: App, response: Response):
        self.view = view
        self.request = request
        self.app = app
        self.response = response

    def handle(self, _):
        from config.database import Model
        self.app.make('HookHandler').fire('*ExceptionHook')

        dump_objs = []
        for dump_name in self.app.make('ObjDumpList'):
            obj = self.app.make(dump_name)
            dump_objs.append(
                {
                    'obj': obj,
                    'members': inspect.getmembers(obj, predicate=inspect.ismethod),
                    'properties': inspect.getmembers(obj),
                }
            )

        self.response.view(self.view.render(
            '/masonite/snippets/exceptions/dump', {
                'objs': dump_objs,
                'type': type,
                'list': list,
                'inspect': inspect,
                'hasattr': hasattr,
                'getattr': getattr,
                'Model': Model,
                'isinstance': isinstance,
                'show_methods': (bool, str, list, dict),
                'len': len,
            }))
