"""Exception Handler Module.

A module for controlling exceptions handling when an error occurs doing executing
code in a Masonite application. These errors could are thrown during runtime.
"""

import os
import platform
import sys
import traceback

from config import application

package_directory = os.path.dirname(os.path.realpath(__file__))


class ExceptionHandler:
    """Class for handling exceptions thrown during runtime."""

    def __init__(self, app):
        """ExceptionHandler constructor. Also responsible for loading static files into the container.

        Arguments:
            app {masonite.app.App} -- Container object
        """
        self._app = app

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

        self._render()

    def _render(self):
        """Render an exception view if the DEBUG configuration is True. Else this should not return anything.

        Returns:
            None
        """
        request = self._app.make('Request')
        request.status(500)

        # Run Any Framework Exception Hooks
        self._app.make('HookHandler').fire('*ExceptionHook')

        # Check if DEBUG is False
        if not application.DEBUG:
            return

        # return a view
        rendered_view = self._app.make('View')('/masonite/snippets/exception',
                                               {
                                                   'exception': self._exception,
                                                   'traceback': traceback,
                                                   'tb': sys.exc_info(),
                                                   'app': self._app,
                                                   'enumerate': enumerate,
                                                   'open': open,
                                                   'platform': platform
                                               }
                                               ).rendered_template
        self._app.bind('Response', rendered_view)
        request.header('Content-Type', str(len(rendered_view)))
