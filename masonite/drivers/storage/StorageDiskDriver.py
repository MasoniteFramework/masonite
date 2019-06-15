import os
import pathlib
import shutil

from masonite import Upload
from masonite.contracts import StorageContract
from masonite.drivers import BaseDriver


class StorageDiskDriver(BaseDriver, StorageContract):

    def put(self, location, contents):
        with open(location, 'w+') as file:
            file.write(contents)

    def append(self, location, contents):
        with open(location, 'a+') as file:
            file.write(contents)

    def get(self, location):
        with open(location) as f:
            return f.read()

    def delete(self, location):
        try:
            os.remove(location)
            return True
        except FileNotFoundError:
            return False

    def exists(self, location):
        return pathlib.Path(location).exists()

    def size(self, location):
        try:
            return os.path.getsize(location)
        except FileNotFoundError:
            return 0

    def extension(self, location):
        return pathlib.Path(location).suffix.replace('.', '')

    def url(self, location):
        pass

    def name(self, location):
        return pathlib.Path(location).name

    def upload(self, *args, **kwargs):
        from wsgi import container
        return container.make(Upload).driver('disk').store(*args, **kwargs)

    def all(self):
        pass

    def make_directory(self, location):
        location = os.path.join(os.getcwd(), location)
        if os.path.isdir(location):
            return True

        os.mkdir(location)
        return True

    def delete_directory(self, directory, force=False):
        if force:
            shutil.rmtree(directory)
            return True
        try:
            pathlib.Path(directory).rmdir()
            return True
        except FileNotFoundError:
            return True

    def move(self, old, new):
        return shutil.move(old, new)
