"""Session Cookie Module."""

import json
from email import message

from ...contracts import SessionContract
from ...drivers import BaseDriver
from ...helpers import config
from ...request import Request


class SessionCookieDriver(SessionContract, BaseDriver):
    """Cookie Session Driver."""

    def __init__(self, request: Request):
        """Cookie Session Constructor.

        Arguments:
            Environ {dict} -- The WSGI environment
            Request {masonite.request.Request} -- The Request class.
        """
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

    def all(self, flash_only=False):
        """Get all session data.

        Returns:
            dict
        """
        return self.__collect_data(flash_only=flash_only)

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

    def __collect_data(self, flash_only=False):
        """Collect data from session and flash data.

        Returns:
            dict
        """
        cookies = {}
        if 'HTTP_COOKIE' in self.request.environ and self.request.environ['HTTP_COOKIE']:
            cookies_original = self.request.environ['HTTP_COOKIE'].split(';')
            for cookie in cookies_original:
                if flash_only:
                    if cookie.strip().startswith('f_'):
                        data = cookie.split("=", 1)
                        cookie_name = data[0].replace('s_', '').replace('f_', '').strip()
                        cookies.update({cookie_name: self.get(cookie_name)})
                else:
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
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        self.request.cookie('f_{0}'.format(key), value, expires=config('session.drivers.cookie.flash_expires', '2 seconds'))

    def get_error_messages(self):
        """Should get and delete the flashed messages

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        only_messages = []
        messages = self.all(flash_only=True).get('errors', {}).items()
        for key, messages in messages:
            for error_message in messages:
                only_messages.append(error_message)
        self.reset(flash_only=True)
        return only_messages

    def get_flashed_messages(self, key, value):
        """Should get and delete the flashed messages

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        messages = self.all(flash_only=True)
        self.reset(flash_only=True)
        return messages

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
