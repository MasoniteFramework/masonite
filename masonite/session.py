

class Session():
    """
    Class Session for manage sessions of the app
    """
    _session = {}

    def __init__(self, environ):
        """
        Constructor
        """
        self.environ = environ

    def get(self, key):
        """
        Get a session from object _session
        """
        ip = self.__get_client_address()
        try:
            session = self._session[ip][key]
        except KeyError:
            session = None

        return session

    def set(self, key, value):
        """
        Set a new session in object _session
        """
        ip = self.__get_client_address()
        if not (ip in self._session):
            self._session[ip] = {}

        self._session[ip][key] = value

    def reset(self):
        """
        Reset object _session
        """
        self._session = {}

    def __get_client_address(self):
        """
        Get ip from the client
        """
        try:
            return self.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            return self.environ['REMOTE_ADDR']
