class Manager(object):

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
        return self.container.resolve(self.manage_driver)

    def create_driver(self, driver=None):
        pass
