

class Session():
    """
    Class Session for manage sessions of the app
    """

    _session = {}
    _flash = {}


    def __init__(self, environ):
        """
        Constructor
        """

        self.environ = environ


    def get(self, key):
        """
        Get a session from object _session
        """

        data = self.__collect_data(key)
        if data:
            return data
        
        return None


    def set(self, key, value):
        """
        Set a new session in object _session
        """

        ip = self.__get_client_address()

        if not ip in self._session:
            self._session[ip] = {}

        self._session[ip][key] = value


    def has(self, key):
        """
        Check if a key exists in the session
        """
        
        data = self.__collect_data()
        if data and key in data:
            return True
        
        return False


    def all(self):
        """
        Get all session data
        """

        return self.__collect_data()


    def flash(self, key, value):
        """
        Add temporary data to the session
        """

        ip = self.__get_client_address()
        if not ip in self._flash:
            self._flash[ip] = {}

        self._flash[ip][key] = value


    def reset(self, flash_only=False):
        """
        Reset object _session
        """

        ip = self.__get_client_address()

        if flash_only:
            if ip in self._flash:
                self._flash[ip] = {}
        else:
            if ip in self._session:
                self._session[ip] = {}


    def __get_client_address(self):
        """
        Get ip from the client
        """

        if 'HTTP_X_FORWARDED_FOR' in self.environ:
            return self.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        
        return self.environ['REMOTE_ADDR']


    def __collect_data(self, key=False):
        """
        Collect data from session and flash data
        """

        ip = self.__get_client_address()

        session = {}

        if ip in self._session:
            session = self._session[ip]
        
        if ip in self._flash:
            session.update(self._flash[ip])

        if key and key in session:
            return session[key]
        
        if not session:
            return None

        return session
        

    def helper(self):
        """
        Used to create builtin helper function
        """

        return self
