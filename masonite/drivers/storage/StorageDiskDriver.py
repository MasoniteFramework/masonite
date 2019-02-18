from masonite.drivers import BaseDriver
from masonite.contracts import StorageContract
import os
import pathlib
from masonite.helpers.filesystem import make_directory



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
        return pathlib.Path(location).suffix

    def url(self, location):
        pass

    def download(self, location): 
        from wsgi import container
        container.make('Request').header({
            'Content-Description': 'File Transfer',
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename={}'.format(self.name(location)),
            'Content-Transfer-Encoding': 'binary',
            # 'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
        })
        from wsgi import container
        request = container.make('Request')

        # with open(location, "rb") as imageFile:
        #     return str(imageFile.read(), 'utf-8')

        fin = open(location, "rb") 
        size = os.path.getsize(location) 
        # start_response("200 OK", [('Content-Type', 'application/zip'), ('Content-length', str(size)), ('Content-Disposition', 'attachment; filename=' + finalModelName + '.zip')])  # return the entire file 
        if 'wsgi.file_wrapper' in request.environ: 
            print('has file wrapper', request.environ['wsgi.file_wrapper'](fin, 1024))
            return request.environ['wsgi.file_wrapper'](fin, 1024) 
        else:
            print('nadaa')

    def name(self, location):
        return pathlib.Path(location).name

    def upload(self): pass
    def all(self): pass

    def make_directory(self, location):
        return make_directory(location)

    def delete_directory(self): pass
    def move(self): pass
