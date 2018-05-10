from masonite.contracts.SessionContract import SessionContract
from masonite.drivers.BaseDriver import BaseDriver


class SessionCookieDriver(SessionContract, BaseDriver):
    """
    Session from the memory driver
    """

    def __init__(self, Environ, Request):
        """
        Constructor
        """

        self.environ = Environ
        self.request = Request

    def get(self, key):
        """
        Get a session from object _session
        """

        cookie = self.request.get_cookie('s_{0}'.format(key))
        if cookie:
            return cookie

        return None

    def set(self, key, value):
        """
        Set a new session in object _session
        """

        self.request.cookie('s_{0}'.format(key), value)

    def has(self, key):
        """
        Check if a key exists in the session
        """

        if self.get(key):
            return True
        return False

    def all(self):
        """
        Get all session data
        """

        return self.__collect_data()
    
    def delete(self, key):
        data = self.__collect_data()

        if self.request.get_cookie('s_{}'.format(key)):
            self.request.delete_cookie('s_{}'.format(key))
            return True
        
        return False

    def __collect_data(self):
        """
        Collect data from session and flash data
        """

        cookies = {}
        if 'HTTP_COOKIE' in self.environ and self.environ['HTTP_COOKIE']:
            cookies_original = self.environ['HTTP_COOKIE'].split(';')
            for cookie in cookies_original:
                if cookie.startswith('s_'):
                    data = cookie.split("=")
                    cookie_value = self.request.get_cookie(data[0])
                    cookies[data[0][2:]] = cookie_value
        return cookies

    def flash(self, key, value):
        """
        Add temporary data to the session
        """

        self.request.cookie('s_{0}'.format(key), value, expires='2 seconds')

    def reset(self, flash_only=False):
        """
        Reset object _session
        """
        cookies = self.__collect_data()
        for cookie in cookies:
            self.request.delete_cookie('s_{0}'.format(cookie))

    def helper(self):
        """
        Used to create builtin helper function
        """

        return self
