""" Session Cookie Module """

import json

from masonite.contracts.SessionContract import SessionContract
from masonite.drivers.BaseDriver import BaseDriver


class SessionCookieDriver(SessionContract, BaseDriver):
    """Cookie Session Driver
    """

    def __init__(self, Environ, Request):
        """Cookie Session Constructor

        Arguments:
            Environ {dict} -- The WSGI environment
            Request {masonite.request.Request} -- The Request class.
        """

        self.environ = Environ
        self.request = Request

    def get(self, key):
        """Get a value from the session.

        Arguments:
            key {string} -- The key to get from the session.

        Returns:
            string|None - Returns None if a value does not exist.
        """

        cookie = self.request.get_cookie('s_{0}'.format(key))
        if cookie:
            return self._get_serialization_value(cookie)

        return None

    def set(self, key, value):
        """Set a vlue in the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """

        if isinstance(value, dict):
            value = json.dumps(value)

        self.request.cookie('s_{0}'.format(key), value)

    def has(self, key):
        """Check if a key exists in the session

        Arguments:
            key {string} -- The key to check for in the session.

        Returns:
            bool
        """

        if self.get(key):
            return True
        return False

    def all(self):
        """Get all session data

        Returns:
            dict
        """

        return self.__collect_data()

    def delete(self, key):
        """Delete a value in the session by it's key.

        Arguments:
            key {string} -- The key to find in the session.

        Returns:
            bool -- If the key was deleted or not
        """

        data = self.__collect_data()

        if self.request.get_cookie('s_{}'.format(key)):
            self.request.delete_cookie('s_{}'.format(key))
            return True

        return False

    def __collect_data(self):
        """Collect data from session and flash data

        Returns:
            dict
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
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """

        if isinstance(value, dict):
            value = json.dumps(value)

        self.request.cookie('s_{0}'.format(key), value, expires='2 seconds')

    def reset(self, flash_only=False):
        """Deletes all session data

        Keyword Arguments:
            flash_only {bool} -- If only flash data should be deleted. (default: {False})
        """

        cookies = self.__collect_data()
        for cookie in cookies:
            self.request.delete_cookie('s_{0}'.format(cookie))

    def helper(self):
        """Used to create builtin helper function
        """

        return self

    def _get_serialization_value(self, value):
        try:
            return json.loads(value)
        except ValueError:
            return value
