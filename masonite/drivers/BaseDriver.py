class BaseDriver:
    _manager = None

    def driver(self, driver):
        return self._manager.driver(driver)
    
    def load_manager(self, manager):
        self._manager = manager
        return self