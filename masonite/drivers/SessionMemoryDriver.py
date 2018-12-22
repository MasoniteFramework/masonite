"""Session Memory Module."""

from masonite.contracts import SessionContract
from masonite.drivers import BaseDriver
from masonite.app import App


class SessionMemoryDriver(SessionContract, BaseDriver):
    """Memory Session Driver."""

    _session = {}
    _flash = {}

    def __init__(self, app: App):
        """Cookie Session Constructor.

        Arguments:
            Environ {dict} -- The WSGI environment
        """
        self.environ = app.make('Environ')

    def get(self, key):
        """Get a value from the session.

        Arguments:
            key {string} -- The key to get from the session.

        Returns:
            string|None - Returns None if a value does not exist.
        """
        data = self.__collect_data(key)
        if data:
            return data

        return None

    def set(self, key, value):
        """Set a vlue in the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        ip = self.__get_client_address()

        if ip not in self._session:
            self._session[ip] = {}

        self._session[ip][key] = value

    def has(self, key):
        """Check if a key exists in the session.

        Arguments:
            key {string} -- The key to check for in the session.

        Returns:
            bool
        """
        data = self.__collect_data()
        if data and key in data:
            return True
        return False

    def all(self):
        """Get all session data.

        Returns:
            dict
        """
        return self.__collect_data()

    def flash(self, key, value):
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        ip = self.__get_client_address()
        if ip not in self._flash:
            self._flash[ip] = {}

        self._flash[ip][key] = value

    def reset(self, flash_only=False):
        """Delete all session data.

        Keyword Arguments:
            flash_only {bool} -- If only flash data should be deleted. (default: {False})
        """
        ip = self.__get_client_address()

        if flash_only:
            if ip in self._flash:
                self._flash[ip] = {}
        else:
            if ip in self._session:
                self._session[ip] = {}

    def delete(self, key):
        """Delete a value in the session by it's key.

        Arguments:
            key {string} -- The key to find in the session.

        Returns:
            bool -- If the key was deleted or not
        """
        data = self.__collect_data()

        if key in data:
            del data[key]
            return True

        return False

    def __get_client_address(self):
        """Get ip from the client."""
        if 'HTTP_X_FORWARDED_FOR' in self.environ:
            return self.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()

        return self.environ['REMOTE_ADDR']

    def __collect_data(self, key=False):
        """Collect data from session and flash data.

        Returns:
            dict
        """
        ip = self.__get_client_address()

        # Declare a new dictionary
        session = {}

        # If the session data has keys
        if ip in self._session:
            session = self._session[ip]

        # If the session flash has keys
        if ip in self._flash:
            session.update(self._flash[ip])

        # If a key is set and it is inside the new declared session, return that key
        if key and key in session:
            return session[key]

        # If the key is set and is not in the session
        if key and key not in session:
            return None

        # If the session is still an empty dictionary
        if not session:
            return None

        # No checks have been hit. Return the new dictionary
        return session

    def helper(self):
        """Used to create builtin helper function."""
        return self
