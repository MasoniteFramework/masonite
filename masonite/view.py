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

    def __init__(self, container):
        self.dictionary = {}
        self.composers = {}
        self.cache = False
        self.container = container
        self.cache_time = None
        self.cache_type = None
        self.template = None
        self.env = Environment(
            loader=PackageLoader('resources', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

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
        self.cache = True
        self.cache_time = float(time)
        self.cache_type = type
        if self.__is_expired_cache():
            self.__create_cache_template(self.template)
        return self

    def __create_cache_template(self, template):
        """
        Save in the cache the template
        """

        cache_type = self.cache_type.lower()
        calc = 0
        if cache_type == "second" or cache_type == "seconds":
            # Set time now for
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
            # If is forever
            return True

        cache_for_time = self.cache_time * calc

        cache_for_time = cache_for_time + time.time()

        self.container.make('Cache').store(
            template + ":" + str(cache_for_time),
            self.rendered_template, '.html',
        )

    def __cached_template_exists(self):
        """
        Check if the cache template exists
        """

        return self.container.make('Cache').cache_exists(self.template)

    def __is_expired_cache(self):
        """
        Check if cache is expired
        """

        # Check if cache_for is set and configurate
        if self.cache_time is None or self.cache_type is None and self.cache:
            return True

        driver_cache = self.container.make('Cache')

        # True is expired
        return not driver_cache.is_valid(self.template)

    def __get_cached_template(self):
        """
        Return the rendered template
        """
        driver_cache = self.container.make('Cache')
        self.rendered_template = driver_cache.get(self.template)
        return self
