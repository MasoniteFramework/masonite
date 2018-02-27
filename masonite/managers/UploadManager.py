from masonite.managers.Manager import Manager
from masonite.exceptions import DriverNotFound, MissingContainerBindingNotFound


class UploadManager(Manager):
    """
    Upload files manager class
    """

    def create_driver(self, driver=None):
        if not driver:
            driver = self.container.make('StorageConfig').DRIVER.capitalize()
        else:
            driver = driver.capitalize()

        try:
            self.manage_driver = self.container.make(
                'Upload{0}Driver'.format(driver))
        except MissingContainerBindingNotFound:
            raise DriverNotFound(
                'Could not find the Upload{0}Driver from the service container. Are you missing a service provider?'.format(driver))
