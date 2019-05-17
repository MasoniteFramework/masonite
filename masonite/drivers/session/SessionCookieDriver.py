"""Session Cookie Module."""

import json

from masonite.contracts import SessionContract
from masonite.drivers import BaseDriver
from masonite.request import Request
from masonite.app import App


class SessionCookieDriver(SessionContract, BaseDriver):
    """Cookie Session Driver."""

    def __init__(self, request: Request, app: App):
        """Cookie Session Constructor.

        Arguments:
            Environ {dict} -- The WSGI environment
            Request {masonite.request.Request} -- The Request class.
        """
        self.environ = app.make('Environ')
        self.request = request

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

        cookie = self.request.get_cookie('f_{0}'.format(key))
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
        """Check if a key exists in the session.

        Arguments:
            key {string} -- The key to check for in the session.

        Returns:
            bool
        """
        if self.get(key):
            return True
        return False

    def all(self):
        """Get all session data.

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
        self.__collect_data()

        if self.request.get_cookie('s_{}'.format(key)):
            self.request.delete_cookie('s_{}'.format(key))
            return True

        return False

    def __collect_data(self):
        """Collect data from session and flash data.

        Returns:
            dict
        """
        cookies = {}
        if 'HTTP_COOKIE' in self.environ and self.environ['HTTP_COOKIE']:
            cookies_original = self.environ['HTTP_COOKIE'].split(';')
            for cookie in cookies_original:
                if cookie.strip().startswith('s_') or cookie.strip().startswith('f_'):
                    data = cookie.split("=", 1)
                    cookie_name = data[0].replace('s_', '').replace('f_', '').strip()
                    cookies.update({cookie_name: self.get(cookie_name)})
        return cookies

    def flash(self, key, value):
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)

        self.request.cookie('f_{0}'.format(key), value, expires='2 seconds')

    def reset(self, flash_only=False):
        """Delete all session data.

        Keyword Arguments:
            flash_only {bool} -- If only flash data should be deleted. (default: {False})
        """
        cookies = self.__collect_data()
        for cookie in cookies:
            if flash_only:
                self.request.delete_cookie('f_{0}'.format(cookie))
                continue

            self.request.delete_cookie('s_{0}'.format(cookie))

    def helper(self):
        """Use to create builtin helper function."""
        return self

    def _get_serialization_value(self, value):
        try:
            return json.loads(value)
        except ValueError:
            return value
