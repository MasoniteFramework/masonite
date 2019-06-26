"""Exception Handler Module.

A module for controlling exceptions handling when an error occurs doing executing
code in a Masonite application. These errors could are thrown during runtime.
"""

import inspect
import os
import platform
import sys
import traceback

from masonite.app import App
from masonite.exceptions import DumpException
from masonite.request import Request
from masonite.response import Response
from masonite.view import View

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
        self._app.make('Storage').STATICFILES.update(
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

    def handle(self, _):
        """Render an exception view if the DEBUG configuration is True. Else this should not return anything.

        Returns:
            None
        """
        request = self._app.make('Request')
        request.status(500)

        # Run Any Framework Exception Hooks
        self._app.make('HookHandler').fire('*ExceptionHook')

        # Check if DEBUG is False
        from config import application
        if not application.DEBUG:
            return

        exc_type, _, _ = sys.exc_info()
        # return a view
        if request.header('Content-Type') == 'application/json':
            stacktrace = []
            for stack in traceback.extract_tb(sys.exc_info()[2]):
                stacktrace.append("{} line {} in {}".format(stack[0], stack[1], stack[2]))

            if hasattr(exc_type, 'file'):
                stacktrace.append("{} line {} in {}".format(exc_type.file, exc_type.tb[1], exc_type.tb[2]))

            self.response.view({'error': {'exception': str(self._exception), 'status': 500, 'stacktrace': stacktrace}}, status=request.get_status())
            return

        if hasattr(exc_type, 'file'):
            last_stacktrace = [[exc_type.file, exc_type.tb[-1][1], exc_type.tb[-1][2]]]
            second_to_last_stacktrace = [[exc_type.file, exc_type.tb[-2][1], exc_type.tb[-2][2]]]
        else:
            last_stacktrace = []
            second_to_last_stacktrace = []

        self.response.view(self._app.make('View')('/masonite/snippets/exception',
                                               {
                                                   'exception': self._exception,
                                                   'split_exception': str(self._exception).split(' '),
                                                   'traceback': traceback,
                                                   'tb': sys.exc_info(),
                                                   'stacktrace': traceback.extract_tb(sys.exc_info()[2]) + last_stacktrace + second_to_last_stacktrace,
                                                   'second_to_last': second_to_last_stacktrace,
                                                   'app': self._app,
                                                   'enumerate': enumerate,
                                                   'open': open,
                                                   'platform': platform
                                               }
        ))


class DD:

    def __init__(self, container):
        self.app = container

    def dump(self, obj):
        self.app.bind('ObjDump', obj)
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

        self.response.view(self.view.render(
            '/masonite/snippets/exceptions/dump', {
                'obj': self.app.make('ObjDump'),
                'type': type,
                'list': list,
                'inspect': inspect,
                'members': inspect.getmembers(self.app.make('ObjDump'), predicate=inspect.ismethod),
                'properties': inspect.getmembers(self.app.make('ObjDump')),
                'hasattr': hasattr,
                'getattr': getattr,
                'Model': Model,
                'isinstance': isinstance,
                'show_methods': (bool, str, list, dict),
                'len': len,
            }))
