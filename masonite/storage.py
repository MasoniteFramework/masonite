"""Module for Storage class."""

import os

from config import application, storage


class Storage:
    """Responsible for compiling Sass."""

    def __init__(self):
        """Storage constructor."""
        pass

    def compile_sass(self):
        """Compile sass."""
        try:
            import sass
        except ImportError:
            pass
        else:
            matches = []
            for files in storage.SASSFILES['importFrom']:
                for root, dirnames, filenames in os.walk(os.path.join(application.BASE_DIRECTORY, files)):
                    for filename in filenames:
                        if filename.endswith(('.sass', '.scss')) and not filename.startswith('_'):
                            matches.append(os.path.join(root, filename))

            for filename in matches:
                with open(filename) as f:
                    compiled_sass = sass.compile(
                        string=f.read(), include_paths=storage.SASSFILES['includePaths']
                    )
                    name = filename.split(
                        os.sep)[-1].replace('.scss', '').replace('.sass', '')
                    write_file = os.path.join(os.path.join(application.BASE_DIRECTORY,
                                                           storage.SASSFILES['compileTo']), '{0}.css'.format(name))
                with open(write_file, 'w') as r:
                    r.write(compiled_sass)
