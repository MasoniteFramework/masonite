from abc import ABC as Contract
from abc import abstractmethod


class StorageContract(Contract):

    @abstractmethod
    def put(self, location, contents):
        """Puts a file into the correct directory

        Arguments:
            location {string} -- The location of the file
            contents {string|object|file-like object} -- The file object to add.
        """
        pass

    @abstractmethod
    def get(self, location):
        """Get the file contents

        Arguments:
            location {string} -- The location of the file
        """
        pass

    @abstractmethod
    def append(self, location, contents):
        """Get the file contents

        Arguments:
            location {string} -- The location of the file.
            contents {string|object|file-like object} -- The file object to add.
        """
        pass

    @abstractmethod
    def delete(self, location):
        """Deletes the file.

        Arguments:
            location {string} -- The location of the file.
        """
        pass

    @abstractmethod
    def exists(self, location):
        """Checks if a file exists.

        Arguments:
            location {string} -- The location of the file.
        """
        pass

    @abstractmethod
    def driver(self):
        pass

    @abstractmethod
    def url(self, location):
        """Gets the full URL of the file to be served.

        Arguments:
            location {string} -- The location of the file.
        """
        pass

    @abstractmethod
    def size(self, location):
        """Gets the size of the file.

        Arguments:
            location {string} -- The location of the file.
        """
        pass

    @abstractmethod
    def extension(self, location):
        """Gets the extension of the file.

        Arguments:
            location {string} -- The location of the file.
        """
        pass

    @abstractmethod
    def upload(self, *args, **kwargs):
        """Passes all arguments to the upload version of this storage driver.

        Arguments:
            location {string} -- The location of the file.
        """
        pass

    @abstractmethod
    def all(self, location):
        """Gets all files in a specific directory

        Arguments:
            location {string} -- The location of the directory.
        """
        pass

    @abstractmethod
    def make_directory(self, directory):
        """Make an empty directory

        Arguments:
            directory {string} -- The location of the directory.
        """
        pass

    @abstractmethod
    def delete_directory(self, directory, force=False):
        """Delete a directory.

        Arguments:
            directory {string} -- The location of the directory

        Keyword Arguments:
            force {bool} -- Whether or not a directory with contents should be deleted. (default: {False})
        """
        pass

    @abstractmethod
    def move(self, old, new):
        """Move a file from 1 location to another.

        Arguments:
            old {string} -- The file of the file object to be moved.
            new {string} -- The location where the file object should be moved to.
        """
        pass

    @abstractmethod
    def name(self, location):
        """Gets the name of the file with the extension

        Arguments:
            location {string} -- The location of the file
        """
        pass
