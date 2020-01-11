import os
import sys
from pydoc import ErrorDuringImport
from cleo import Application
from .commands import NewCommand, InstallCommand
from . import __version__

sys.path.append(os.getcwd())

application = Application('Masonite Version:', __version__)
application.add(NewCommand())
application.add(InstallCommand())


try:
    from wsgi import container
    from cleo import Command
    for key, value in container.collect(Command).items():
        application.add(value)
except ErrorDuringImport as e:
    print(e)
except ImportError:
    pass

if __name__ == '__main__':
    application.run()
