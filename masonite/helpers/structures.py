"""A Module For Manipulating Code Structures."""

import pydoc
import inspect


class Dot:

    def dot(self, search, dictionary, default=None):
        """The search string in dot notation to look into the dictionary for.

        Arguments:
            search {string} -- This should be a string in dot notation like 'key.key.value'.
            dictionary {dict} -- A normal dictionary which will be searched using the search string in dot notation.

        Keyword Arguments:
            default {string} -- The default value if nothing is found in the dictionary. (default: {None})

        Returns:
            string -- Returns the value found the dictionary or the default value specified above if nothing is found.
        """
        if '.' not in search:
            if search == '':
                return dictionary
            # print('search', search, 'dictionary', dictionary)
            return dictionary[search]

        searching = search.split('.')
        while len(searching) > 0:
            dic = dictionary
            for search in searching:
                if not dic:
                    return default
                dic = dic.get(search)

            if not isinstance(dic, dict):
                return dic

            del searching[-1]

    def locate(self, search_path, default=''):
        """Locate the object from the given search path

        Arguments:
            search_path {string} -- A search path to fetch the object from like config.application.debug.

        Keyword Arguments:
            default {string} -- A default string if the search path is not found (default: {''})

        Returns:
            any -- Could be a string, object or anything else that is fetched.
        """
        value = self.find(search_path, default)

        if isinstance(value, dict):
            return self.dict_dot('.'.join(search_path.split('.')[3:]), value, default)

        if value is not None:
            return value

        return default

    def dict_dot(self, search, dictionary, default):
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
            search_path {string} -- The search path to find the module, dictionary key, object etc.
                                    This is typically in the form of dot notation 'config.application.debug'

        Keyword Arguments:
            default {string} -- The default value to return if the search path could not be found. (default: {''})

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
    return Dot().locate('config.' + path, default)
