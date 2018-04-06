

class Session():
    """
    Class Session for manage sessions of the app
    """

    _session = dict()
    _flash = dict()


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
            self._session[ip] = dict()

        self._session[ip][key] = value


    def has(self, key):
        if self.get(key):
            return True
        
        return False


    def all(self):
        ip = self.__get_client_address()
        return self._session[ip]


    def flash(self, key, value):
        ip = self.__get_client_address()
        if not (ip in self._flash):
            self._flash[ip] = dict()

        self._flash[ip][key] = value


    def reset(self, flash_only=False):
        """
        Reset object _session
        """

        ip = self.__get_client_address()

        if flash_only:
            if ip in self._flash:
                self._flash[ip] = dict()
        else:
            if ip in self._session:
                self._session[ip] = dict()

    def __get_client_address(self):
        """
        Get ip from the client
        """

        if 'HTTP_X_FORWARDED_FOR' in self.environ:
            return self.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        
        return self.environ['REMOTE_ADDR']


    def __collect_data(self, key):
        ip = self.__get_client_address()

        session = dict()

        if ip in self._session:
            session = self._session[ip]
        
        if ip in self._flash:
            session.update(self._flash[ip])

        if key in session:
            return session[key]
        
        return None
        

    def helper(self):
        """
        Used to create builtin helper function
        """

        return self
