from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from masonite.exceptions import RequiredContainerBindingNotFound


def view(template='index', dictionary={}):
    env = Environment(
        loader=PackageLoader('resources', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    return env.get_template(template + '.html').render(dictionary)


class View:
    """
    Render template view
    """

    def __init__(self, container):
        self.dictionary = {}
        self.composers = {}
        self.container = container

        # If the cache_for method is declared
        self.cache = False
        # Cache time of cache_for
        self.cache_time = None
        # Cache type of cache_for
        self.cache_type = None

        self.template = None
        self.env = Environment(
            loader=PackageLoader('resources', 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
            extensions=['jinja2.ext.loopcontrols']
        )

    def render(self, template, dictionary={}):
        """
        Get the string contents of the view.
        """

        filename = template + '.html'

        if template.startswith('/'):
            location = template.split('/')
            filename = location[-1] + '.html'

            # If the location is more than 1 directory deep
            if len(location[1:-1]) > 1:
                loader = PackageLoader(*location[1:-1])
            else:
                loader = FileSystemLoader(str('/'.join(location[1:-1]) + '/'))
            
            self.env = Environment(
                loader=loader,
                autoescape=select_autoescape(['html', 'xml']),
                extensions=['jinja2.ext.loopcontrols']
            )

        self.dictionary.update(dictionary)

        # Load template
        self.template = template

        # Check if use cache and return template from cache if exists
        if self.container.has('Cache') and self.__cached_template_exists() and not self.__is_expired_cache():
            return self.__get_cached_template()

        if template in self.composers:
            self.dictionary.update(self.composers[template])

        if '*' in self.composers:
            self.dictionary.update(self.composers['*'])

        self.rendered_template = self.env.get_template(filename).render(
            self.dictionary)

        return self

    def composer(self, composer_name, dictionary):
        """
        Updates composer dictionary
        """

        if isinstance(composer_name, str):
            self.composers[composer_name] = dictionary

        if isinstance(composer_name, list):
            for composer in composer_name:
                self.composers[composer] = dictionary

        return self

    def extend(self):
        pass

    def share(self, dictionary):
        """
        Updates the dictionary
        """

        self.dictionary.update(dictionary)
        return self

    def cache_for(self, time=None, type=None):
        """
        Set time and type for cache
        """

        if not self.container.has('Cache'):
            raise RequiredContainerBindingNotFound(
                "The 'Cache' container binding is required to use this method and wasn't found in the container. You may be missing a Service Provider"
            )

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

        self.container.make('Cache').store_for(
            template, self.rendered_template,
            self.cache_time, self.cache_type, '.html',
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
