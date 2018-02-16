import os

class UploadDiskDriver(object):

    def __init__(self, StorageConfig, Application):
        self.config = StorageConfig
        self.appconfig = Application

    def store(self, fileitem, location=None):
        filename = os.path.basename(fileitem.filename)

        if not location:
            location = self.config.DRIVERS['disk']['location']
        
        open(location + filename, 'wb').write(fileitem.file.read())

        return location + filename

    def storePrepend(self, fileitem, prepend, location=None):
        filename = os.path.basename(fileitem.filename)

        if not location:
            location = self.config.DRIVERS['disk']['location']

        open(location + prepend + filename, 'wb').write(fileitem.file.read())

        return location + prepend + filename
