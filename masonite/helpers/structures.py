"""A Module For Manipulating Code Structures."""

import pydoc
import inspect
from orator.support.collection import Collection as collect


class Dot:

    def dot(self, search, dictionary, default=None):
        """The search string in dot notation to look into the dictionary for.

        Arguments:
            search {string} -- This should be a string in dot notation
                                like 'key.key.value'.
            dictionary {dict} -- A normal dictionary which will be searched using
                                the search string in dot notation.

        Keyword Arguments:
            default {string} -- The default value if nothing is found
                                in the dictionary. (default: {None})

        Returns:
            string -- Returns the value found the dictionary or the default
                        value specified above if nothing is found.
        """
        if '.' not in search:
            if search == '':
                return dictionary
            try:
                return dictionary[search]
            except KeyError:
                return default

        searching = search.split('.')
        possible = None
        while searching:
            dic = dictionary
            for value in searching:
                if not dic:
                    if '*' in searching:
                        return []
                    return default

                if isinstance(dic, list):
                    try:
                        return collect(dic).pluck(searching[searching.index('*') + 1]).serialize()
                    except KeyError:
                        return []
                dic = dic.get(value)

                if isinstance(dic, str) and dic.isnumeric():
                    continue

                if dic and not isinstance(dic, int) and len(dic) == 1 and not isinstance(dic[list(dic)[0]], dict):
                    possible = dic

            if not isinstance(dic, dict):
                return dic

            del searching[-1]
        return possible

    def locate(self, search_path, default=''):
        """Locate the object from the given search path

        Arguments:
            search_path {string} -- A search path to fetch the object
                                    from like config.application.debug.

        Keyword Arguments:
            default {string} -- A default string if the search path is
                                not found (default: {''})

        Returns:
            any -- Could be a string, object or anything else that is fetched.
        """
        value = self.find(search_path, default)

        if isinstance(value, dict):
            return self.dict_dot('.'.join(search_path.split('.')[3:]), value, default)

        if value is not None:
            return value

        return default

    def dict_dot(self, search, dictionary, default=''):
        """Takes a dot notation representation of a dictionary and fetches it from the dictionary.

        This will take something like s3.locations and look into the s3 dictionary and fetch the locations
        key.

        Arguments:
            search {string} -- The string to search for in the dictionary using dot notation.
            dictionary {dict} -- The dictionary to search through.

        Returns:
            string -- The value of the dictionary element.
        """
        return self.dot(search, dictionary, default)

    def find(self, search_path, default=''):
        """Used for finding both the uppercase and specified version.

        Arguments:
            search_path {string} -- The search path to find the module,
                                    dictionary key, object etc. This is typically
                                    in the form of dot notation 'config.application.debug'

        Keyword Arguments:
            default {string} -- The default value to return if the search path
                                could not be found. (default: {''})

        Returns:
            any -- Could be a string, object or anything else that is fetched.
        """
        value = pydoc.locate(search_path)

        if value:
            return value

        paths = search_path.split('.')

        value = pydoc.locate('.'.join(paths[:-1]) + '.' + paths[-1].upper())

        if value:
            return value

        search_path = -1

        # Go backwards through the dot notation until a match is found.
        ran = 0
        while ran < len(paths):
            try:
                value = pydoc.locate('.'.join(paths[:search_path]) + '.' + paths[search_path].upper())
            except IndexError:
                return default

            if value:
                break

            value = pydoc.locate('.'.join(paths[:search_path]) + '.' + paths[search_path])

            if value:
                break

            search_path -= 1
            ran += 1

        if not value or inspect.ismodule(value):
            return default

        return value


def config(path, default=''):
    """Used to fetch a value from a configuration file

    Arguments:
        path {string} -- The search path using dot notation of the value to get

    Keyword Arguments:
        default {str} -- The default value if not value and be found (default: {''})

    Returns:
        mixed
    """
    return Dot().locate('config.' + path, default)
