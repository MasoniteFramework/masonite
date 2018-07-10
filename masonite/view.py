from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader, ChoiceLoader
from jinja2.exceptions import TemplateNotFound
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
        self.environments = []
        self._filters = {}


    def render(self, template, dictionary={}):
        """
        Get the string contents of the view.
        """

        self.__load_environment(template)

        self.dictionary.update(dictionary)

        # Check if use cache and return template from cache if exists
        if self.container.has('Cache') and self.__cached_template_exists() and not self.__is_expired_cache():
            return self.__get_cached_template()

        # Check if composers are even set for a speed improvement
        if self.composers:
            self._update_from_composers()

        self.rendered_template = self.env.get_template(self.filename).render(
            self.dictionary)

        return self

    def _update_from_composers(self):

        # Check if the template is directly specified in the composer
        if self.template in self.composers:
            self.dictionary.update(self.composers[self.template])

        # Check if there is just an astericks in the composer
        if '*' in self.composers:
            self.dictionary.update(self.composers['*'])
        
        # We will append onto this string for an easier way to search through wildcard routes
        compiled_string = ''

        # Check for wildcard view composers
        for template in self.template.split('/'):
            # Append the template onto the compiled_string
            compiled_string += template
            if '{}*'.format(compiled_string) in self.composers:
                self.dictionary.update(self.composers['{}*'.format(compiled_string)])
            else:
                # Add a slash to symbolize going into a deeper directory structure
                compiled_string += '/'


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
    
    def exists(self, template):
        self.__load_environment(template)
        
        try:
            self.env.get_template(self.filename)
            return True
        except TemplateNotFound as e:
            return False
    
    def add_environment(self, template_location, loader=PackageLoader):
        # loader(package_name, location)
        # /dashboard/templates/dashboard
        if loader == PackageLoader:
            template_location = template_location.split('/')

            self.environments.append(loader(template_location[0], '/'.join(template_location[1:])))
        else:
            self.environments.append(
                loader(template_location))
    
    def filter(self, name, function):
        self._filters.update({name: function})

    def __load_environment(self, template):
        self.template = template
        self.filename = template + '.html'

        if template.startswith('/'):
            # Filter blanks strings from the split
            location = list(filter(None, template.split('/')))
            self.filename = location[-1] + '.html'

            loader = PackageLoader(location[0], '/'.join(location[1:-1]))

            self.env = Environment(
                loader=ChoiceLoader(
                        [loader] + self.environments
                    ),
                autoescape=select_autoescape(['html', 'xml']),
                extensions=['jinja2.ext.loopcontrols']
            )
        else:
            self.env = Environment(
                loader=ChoiceLoader(
                    [PackageLoader('resources', 'templates')] +
                    self.environments
                    ),
                autoescape=select_autoescape(['html', 'xml']),
                extensions=['jinja2.ext.loopcontrols']
            )
        
        self.env.filters.update(self._filters)

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
