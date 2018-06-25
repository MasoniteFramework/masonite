
import os
import sys
import time
import subprocess
import threading

import waitress
from cleo import Command


class ServeCommand(Command):
    """
    Run the Masonite server

    serve
        {--port=8000 : Specify which port to run the server}
        {--host=127.0.0.1 : Specify which ip address to run the server}
        {--r|reload : Make the server automatically reload on file changes}
    """

    def handle(self):
        self._check_patch()
        if self.option('reload'):
            self._run_with_reloader(extra_files=[".env"])

        else:
            self._run_application()

    def _run_application(self):
        from wsgi import application
        waitress.serve(
            application,
            host=self.option('host'),
            port=self.option('port'))
    
    def _check_patch(self):
        patched = False

        with open('wsgi.py', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        # change the line that starts with KEY=
        for line_number, line in enumerate(data):
            if line.startswith("for provider in container.make('Providers'):"):
                patched = True
                break
        
        if not patched:
            print('\033[93mWARNING: {}\033[0m'.format(
                "Your application does not have a 2.0 patch! You can read more about this patch here: https://dev.to/josephmancuso/masonite-framework-20-patch-3op2"))

    def _run_with_reloader(self, extra_files=None, interval=1):
        """Run the given function in an independent python interpreter."""
        import signal
        from wsgi import application
        reloader = WatchdogReloaderLoop(extra_files, interval, log_func=self.comment)
        signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
        try:
            if os.environ.get('MASONITE_RUN_MAIN') == 'true':
                t = threading.Thread(target=self._run_application, args=())
                t.setDaemon(True)
                t.start()
                reloader.run()
            else:
                sys.exit(reloader.restart_with_reloader())
        except KeyboardInterrupt:
            pass

'''
|--------------------------------------------------------------------------
| Automatic Reloading Code
|--------------------------------------------------------------------------
|
| The grand majority of this auto-reloading code is based on the automatic
| reloading code provided by Werkzeug. I edited it to remove support for
| Python 2x and to use only Watchdog, since we will know that watchdog
| is present. Additionally, I changed the light logging it had to hook
| into Cleo's logging system.
|
| Werkzeug is licensed under a BSD-like open source license. The original
| work can be found at the link below.
|
| https://github.com/pallets/werkzeug
|
'''

iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))


def _iter_module_files():
    """This iterates over all relevant Python files.  It goes through all
    loaded files from modules, all files in folders of already loaded modules
    as well as all files reachable through a package.
    """
    # The list call is necessary on Python 3 in case the module
    # dictionary modifies during iteration.
    for module in list(sys.modules.values()):
        if module is None:
            continue
        filename = getattr(module, '__file__', None)
        if filename:
            if os.path.isdir(filename) and \
               os.path.exists(os.path.join(filename, "__init__.py")):
                filename = os.path.join(filename, "__init__.py")

            old = None
            while not os.path.isfile(filename):
                old = filename
                filename = os.path.dirname(filename)
                if filename == old:
                    break
            else:
                if filename[-4:] in ('.pyc', '.pyo'):
                    filename = filename[:-1]
                yield filename


def _find_observable_paths(extra_files=None):
    """Finds all paths that should be observed."""
    rv = set(os.path.dirname(os.path.abspath(x))
             if os.path.isfile(x) else os.path.abspath(x)
             for x in sys.path)

    for filename in extra_files or ():
        rv.add(os.path.dirname(os.path.abspath(filename)))

    for module in list(sys.modules.values()):
        fn = getattr(module, '__file__', None)
        if fn is None:
            continue
        fn = os.path.abspath(fn)
        rv.add(os.path.dirname(fn))

    return _find_common_roots(rv)


def _get_args_for_reloading():
    """Returns the executable. This contains a workaround for windows
    if the executable is incorrectly reported to not have the .exe
    extension which can cause bugs on reloading.
    """
    rv = [sys.executable]
    py_script = sys.argv[0]
    if os.name == 'nt' and not os.path.exists(py_script) and \
       os.path.exists(py_script + '.exe'):
        py_script += '.exe'
    if os.path.splitext(rv[0])[1] == '.exe' and os.path.splitext(py_script)[1] == '.exe':
        rv.pop(0)
    rv.append(py_script)
    rv.extend(sys.argv[1:])
    return rv


def _find_common_roots(paths):
    """Out of some paths it finds the common roots that need monitoring."""
    paths = [x.split(os.path.sep) for x in paths]
    root = {}
    for chunks in sorted(paths, key=len, reverse=True):
        node = root
        for chunk in chunks:
            node = node.setdefault(chunk, {})
        node.clear()

    rv = set()

    def _walk(node, path):
        for prefix, child in iteritems(node):
            _walk(child, path + (prefix,))
        if not node:
            rv.add('/'.join(path))
    _walk(root, ())
    return rv


class ReloaderLoop(object):
    name = None

    # monkeypatched by testsuite. wrapping with `staticmethod` is required in
    # case time.sleep has been replaced by a non-c function (e.g. by
    # `eventlet.monkey_patch`) before we get here
    _sleep = staticmethod(time.sleep)

    def __init__(self, extra_files=None, interval=1, log_func=None):
        self.extra_files = set(os.path.abspath(x)
                               for x in extra_files or ())
        self.interval = interval
        self.log_func = log_func

    def _log(self, message):
        if self.log_func:
            self.log_func(' [*] {}'.format(message))

    def run(self):
        pass

    def restart_with_reloader(self):
        """Spawn a new Python interpreter with the same arguments as this one,
        but running the reloader thread.
        """
        while 1:
            self._log('Restarting with %s' % self.name)
            args = _get_args_for_reloading()
            new_environ = os.environ.copy()
            new_environ['MASONITE_RUN_MAIN'] = 'true'

            exit_code = subprocess.call(args, env=new_environ,
                                        close_fds=False)
            if exit_code != 3:
                return exit_code

    def trigger_reload(self, filename):
        self.log_reload(filename)
        sys.exit(3)

    def log_reload(self, filename):
        filename = os.path.abspath(filename)
        self._log('Detected change in %r, reloading' % filename)


class WatchdogReloaderLoop(ReloaderLoop):

    def __init__(self, *args, **kwargs):
        ReloaderLoop.__init__(self, *args, **kwargs)
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        self.observable_paths = set()

        def _check_modification(filename):
            if filename in self.extra_files:
                self.trigger_reload(filename)
            dirname = os.path.dirname(filename)
            if dirname.startswith(tuple(self.observable_paths)):
                if filename.endswith(('.pyc', '.pyo', '.py')):
                    self.trigger_reload(filename)

        class _CustomHandler(FileSystemEventHandler):

            def on_created(self, event):
                _check_modification(event.src_path)

            def on_modified(self, event):
                _check_modification(event.src_path)

            def on_moved(self, event):
                _check_modification(event.src_path)
                _check_modification(event.dest_path)

            def on_deleted(self, event):
                _check_modification(event.src_path)

        reloader_name = Observer.__name__.lower()
        if reloader_name.endswith('observer'):
            reloader_name = reloader_name[:-8]
        reloader_name += ' reloader'

        self.name = reloader_name

        self.observer_class = Observer
        self.event_handler = _CustomHandler()
        self.should_reload = False

    def trigger_reload(self, filename):
        # This is called inside an event handler, which means throwing
        # SystemExit has no effect.
        # https://github.com/gorakhargosh/watchdog/issues/294
        self.should_reload = True
        self.log_reload(filename)

    def run(self):
        watches = {}
        observer = self.observer_class()
        observer.start()

        try:
            while not self.should_reload:
                to_delete = set(watches)
                paths = _find_observable_paths(self.extra_files)
                for path in paths:
                    if path not in watches:
                        try:
                            watches[path] = observer.schedule(
                                self.event_handler, path, recursive=True)
                        except OSError:
                            # Clear this path from list of watches We don't want
                            # the same error message showing again in the next
                            # iteration.
                            watches[path] = None
                    to_delete.discard(path)
                for path in to_delete:
                    watch = watches.pop(path, None)
                    if watch is not None:
                        observer.unschedule(watch)
                self.observable_paths = paths
                self._sleep(self.interval)
        finally:
            observer.stop()
            observer.join()

        sys.exit(3)
