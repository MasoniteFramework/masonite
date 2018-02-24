import glob
import os
import re
import time

from jinja2 import Environment, PackageLoader, select_autoescape


def view(template='index', dictionary={}):
    env = Environment(
        loader=PackageLoader('resources', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    return env.get_template(template + '.html').render(dictionary)


class View(object):
    """
    Render template view
    """

    def __init__(self):
        self.dictionary = {}
        self.composers = {}
        self.container = None
        self.cache_time = None
        self.cache_type = None
        self.template = None
        self.env = Environment(
            loader=PackageLoader('resources', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def load_container(self, container):
        self.container = container
        return self

    def render(self, template, dictionary={}):
        self.dictionary.update(dictionary)

        # Load template
        self.template = template

        # Check if use cache and return template from cache if exists
        if self.__cached_template_exists() and not self.__is_expired_cache():
            return self.__get_cached_template()

        if template in self.composers:
            self.dictionary.update(self.composers[template])

        if '*' in self.composers:
            self.dictionary.update(self.composers['*'])

        filename = template + '.html'
        self.rendered_template = self.env.get_template(filename).render(
            self.dictionary)

        return self

    def composer(self, composer_name, dictionary):

        if isinstance(composer_name, str):
            self.composers[composer_name] = dictionary

        if isinstance(composer_name, list):
            for composer in composer_name:
                self.composers[composer] = dictionary

        return self

    def extend(self):
        pass

    def share(self, dictionary):
        self.dictionary.update(dictionary)
        return self

    def cache_for(self, time=None, type=None):
        """
        Set time and type for cache
        """

        self.cache_time = time
        self.cache_type = type

        if self.__is_expired_cache():
            self.__create_cache_template(self.template)
        return self

    # --------
    # Privates
    # --------

    def __get_path_cache(self):
        """
        Get path location disk config
        """

        cache_config = self.container.make('CacheConfig')
        path = cache_config.DRIVERS['disk']['location'] + "/"
        return path

    def __create_cache_template(self, template):
        """
        Save in the cache the template
        """

        self.container.make('Cache').store(
            template + ":" + str(time.time()) + '.html',
            self.rendered_template
        )

    def __cached_template_exists(self):
        """
        Check if the cache template exists
        """

        path = self.__get_path_cache()
        find_template = glob.glob(path + "/" + self.template + ":*")
        if find_template:
            return True
        return False

    def __is_expired_cache(self):
        """
        Check if cache is expired
        """

        # If is forever
        if self.cache_time is None and self.cache_time is None:
            return False

        # By seconds
        cache_type = self.cache_type.lower()
        calc = 0
        if cache_type == "second" or cache_type == "seconds":
            calc = 1
        elif cache_type == "minutes" or cache_type == "minute":
            calc = 60
        elif cache_type == "hours" or cache_type == 'hour':
            calc = 60 * 60
        elif cache_type == "days" or cache_type == 'day':
            calc = 60 * 60 * 60
        elif cache_type == "months" or cache_type == 'month':
            calc = 60 * 60 * 60 * 60
        elif cache_type == "years" or cache_type == 'year':
            calc = 60 * 60 * 60 * 60 * 60
        else:
            return False

        path = self.__get_path_cache()
        find_template = glob.glob(path + "/" + self.template + ":*")
        if find_template:
            template_file = find_template[0]
        else:
            return True

        time_cache = self.__get_time_cache(template_file)

        result = not (time.time() - float(time_cache)) > self.cache_time * calc
        if result:
            self.__delete_cache()
        # True is expired
        return result

    def __delete_cache(self):
        """
        Remove template file from cache
        """

        path_bootstrap_cache = self.__get_path_cache()
        for template in glob.glob(path_bootstrap_cache + self.template+':*'):
            os.remove(template)

    def __get_time_cache(self, template_file):
        """
        Get time from file cache
        """

        time_cache = re.search(
            self.template + ":(.*).html", template_file
        ).group(1)
        return float(time_cache)

    def __get_cached_template(self):
        """
        Return the rendered template
        """

        path_cache = self.__get_path_cache()
        self.rendered_template = open(
            glob.glob(path_cache + self.template + ':*')[0], 'r').read()

        return self
