import pydoc


class Dot:

    def locate(self, search_path, default=''):
        """Locate the object from the given search path

        Arguments:
            path {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        value = self.find(search_path, default)

        if isinstance(value, dict):
            return self.dict_dot('.'.join(search_path.split('.')[3:]), value)

        if value is not None:
            return value

    def dict_dot(self, search, dictionary):
        if "." in search:
            key, rest = search.split(".", 1)
            try:
                return self.dict_dot(dictionary[key], rest)
            except (KeyError, TypeError):
                pass
        else:
            try:
                return dictionary[search]
            except TypeError:
                pass

        return self.dict_dot(dictionary, search)

    def find(self, search_path, default=''):
        """Used for finding both the uppercase and specified version

        Arguments:
            path {string} -- The path to find
        """
        value = pydoc.locate(search_path)
        if value:
            return value

        paths = search_path.split('.')

        value = pydoc.locate('.'.join(paths[:-1]) + '.' + paths[-1].upper())
        if value:
            return value

        search_path = -1
        while search_path < len(paths):
            value = pydoc.locate('.'.join(paths[:search_path]) + '.' + paths[search_path].upper())

            if value:
                break

            value = pydoc.locate('.'.join(paths[:search_path]) + '.' + paths[search_path])

            if value:
                break
            
            if default:
                return default

            search_path -= 1

        return value

def config(path, default=''):
    return Dot().locate(path, default)