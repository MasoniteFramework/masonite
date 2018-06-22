import sys
import traceback
import os
import platform

package_directory = os.path.dirname(os.path.realpath(__file__))


class ExceptionHandler:

    def __init__(self, app):
        self._app = app

        self._register_static_files()
    
    def _register_static_files(self):
        self._app.make('Storage').STATICFILES.update(
            {
                os.path.join(package_directory, 'snippets/exceptions'):
                '_exceptions/'
            }
        )
    
    def load_exception(self, exception):
        self._exception = exception

        self._render()
    
    def _render(self):
        self._app.bind('StatusCode', '500 Internal Server Error')

        # Run Any Framework Exception Hooks
        self._app.make('HookHandler').fire('*ExceptionHook')

        # Check if DEBUG is False
        if not self._app.make('Application').DEBUG or self._app.make('Application').DEBUG == 'False':
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
