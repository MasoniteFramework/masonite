from masonite.exceptions import DriverNotFound, MissingContainerBindingNotFound


class Manager:
    """
    Manager container class
    """

    config = None
    driver_prefix = None

    def __init__(self, container=None):
        self.manage_driver = None
        self.container = container

        if container:
            self.create_driver()

    def load_container(self, container):
        self.container = container
        self.create_driver()
        return self

    def driver(self, driver):
        self.create_driver(driver)
        return self.container.resolve(self.manage_driver).load_manager(self)

    def create_driver(self, driver=None):
        if not driver:
            driver = self.container.make(self.config).DRIVER.capitalize()
        else:
            driver = driver.capitalize()

        try:
            self.manage_driver = self.container.make(
                '{0}{1}Driver'.format(self.driver_prefix, driver)
            )
        except MissingContainerBindingNotFound:
            raise DriverNotFound(
                'Could not find the {0}{1}Driver from the service container. Are you missing a service provider?'.format(self.driver_prefix, driver))
