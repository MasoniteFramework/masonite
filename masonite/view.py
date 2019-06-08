"""View Module."""


from jinja2 import ChoiceLoader, Environment, PackageLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound

from masonite.exceptions import RequiredContainerBindingNotFound, ViewException


class View:
    """View class. Responsible for handling everything involved with views and view environments."""

    _splice = '/'

    def __init__(self, container):
        """View constructor.

        Arguments:
            container {masonite.app.App} -- Container object.
        """
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
        self.extension = '.html'
        self._jinja_extensions = ['jinja2.ext.loopcontrols']
        self._filters = {}
        self._tests = {}
        self._shared = {}

    def render(self, template, dictionary={}):
        """Get the string contents of the view.

        Arguments:
            template {string} -- Name of the template you want to render.

        Keyword Arguments:
            dictionary {dict} -- Data that you want to pass into your view. (default: {{}})

        Returns:
            self
        """
        if not isinstance(dictionary, dict):
            raise ViewException('Second parameter to render method needs to be a dictionary, {} passed.'.format(type(dictionary).__name__))

        self.__load_environment(template)
        self.dictionary = {}

        self.dictionary.update(dictionary)
        self.dictionary.update(self._shared)

        # Check if use cache and return template from cache if exists
        if self.container.has('Cache') and self.__cached_template_exists() and not self.__is_expired_cache():
            return self.__get_cached_template()

        # Check if composers are even set for a speed improvement
        if self.composers:
            self._update_from_composers()

        if self._tests:
            self.env.tests.update(self._tests)

        self.rendered_template = self._render()

        return self

    def _render(self):
        try:
            # Try rendering the template with '.html' appended
            return self.env.get_template(self.filename).render(
                self.dictionary)
        except TemplateNotFound:
            # Try rendering the direct template the user has supplied
            return self.env.get_template(self.template).render(
                self.dictionary)

    def _update_from_composers(self):
        """Add data into the view from specified composers."""
        # Check if the template is directly specified in the composer
        if self.template in self.composers:
            self.dictionary.update(self.composers.get(self.template))

        # Check if there is just an astericks in the composer
        if '*' in self.composers:
            self.dictionary.update(self.composers.get('*'))

        # We will append onto this string for an easier way to search through wildcard routes
        compiled_string = ''

        # Check for wildcard view composers
        for template in self.template.split(self._splice):
            # Append the template onto the compiled_string
            compiled_string += template
            if self.composers.get('{}*'.format(compiled_string)):
                self.dictionary.update(
                    self.composers['{}*'.format(compiled_string)])
            else:
                # Add a slash to symbolize going into a deeper directory structure
                compiled_string += '/'

    def composer(self, composer_name, dictionary):
        """Update composer dictionary.

        Arguments:
            composer_name {string} -- Key to bind dictionary of data to.
            dictionary {dict} -- Dictionary of data to add to controller.

        Returns:
            self
        """
        if isinstance(composer_name, str):
            self.composers[composer_name] = dictionary

        if isinstance(composer_name, list):
            for composer in composer_name:
                self.composers[composer] = dictionary

        return self

    def share(self, dictionary):
        """Share data to all templates.

        Arguments:
            dictionary {dict} -- Dictionary of key value pairs to add to all views.

        Returns:
            self
        """
        self._shared.update(dictionary)
        return self

    def cache_for(self, time=None, cache_type=None):
        """Set time and type for cache.

        Keyword Arguments:
            time {string} -- Time to cache template for (default: {None})
            cache_type {string} -- Type of the cache. (default: {None})

        Raises:
            RequiredContainerBindingNotFound -- Thrown when the Cache key binding is not found in the container.

        Returns:
            self
        """
        if not self.container.has('Cache'):
            raise RequiredContainerBindingNotFound(
                "The 'Cache' container binding is required to use this method and wasn't found in the container. You may be missing a Service Provider"
            )

        self.cache = True
        self.cache_time = float(time)
        self.cache_type = cache_type
        if self.__is_expired_cache():
            self.__create_cache_template(self.template)
        return self

    def exists(self, template):
        """Check if a template exists.

        Arguments:
            template {string} -- Name of the template to check for.

        Returns:
            bool
        """
        self.__load_environment(template)

        try:
            self.env.get_template(self.filename)
            return True
        except TemplateNotFound:
            return False

    def add_environment(self, template_location, loader=PackageLoader):
        """Add an environment to the templates.

        Arguments:
            template_location {string} -- Directory location to attach the environment to.

        Keyword Arguments:
            loader {jinja2.Loader} -- Type of Jinja2 loader to use. (default: {jinja2.PackageLoader})
        """        # loader(package_name, location)
        # /dashboard/templates/dashboard
        if loader == PackageLoader:
            template_location = template_location.split(self._splice)

            self.environments.append(
                loader(template_location[0], '/'.join(template_location[1:])))
        else:
            self.environments.append(
                loader(template_location))

    def filter(self, name, function):
        """Use to add filters to views.

        Arguments:
            name {string} -- Key to bind the filter to.
            function {object} -- Function used for the template filter.
        """
        self._filters.update({name: function})

    def test(self, key, obj):
        self._tests.update({key: obj})
        return self

    def add_extension(self, extension):
        self._jinja_extensions.append(extension)
        return self

    def __load_environment(self, template):
        """Private method for loading all the environments.

        Arguments:
            template {string} -- Template to load environment from.
        """
        self.template = template
        self.filename = template.replace(self._splice, '/').replace('.', '/') + self.extension

        if template.startswith('/'):
            # Filter blanks strings from the split
            location = list(filter(None, template.split('/')))
            self.filename = location[-1] + self.extension

            loader = ChoiceLoader(
                [PackageLoader(location[0], '/'.join(location[1:-1]))] + self.environments
            )
            self.env = Environment(
                loader=loader,
                autoescape=select_autoescape(['html', 'xml']),
                extensions=self._jinja_extensions,
                line_statement_prefix='@'
            )

        else:
            loader = ChoiceLoader(
                [PackageLoader('resources', 'templates')] + self.environments
            )

            # Set the searchpath since some packages look for this object
            # This is sort of a hack for now
            loader.searchpath = ''

            self.env = Environment(
                loader=loader,
                autoescape=select_autoescape(['html', 'xml']),
                extensions=self._jinja_extensions,
                line_statement_prefix='@'
            )

        self.env.filters.update(self._filters)

    def __create_cache_template(self, template):
        """Save in the cache the template.

        Arguments:
            template {string} -- Creates the cached templates.
        """
        self.container.make('Cache').store_for(
            template, self.rendered_template,
            self.cache_time, self.cache_type, '.html',
        )

    def __cached_template_exists(self):
        """Check if the cache template exists.

        Returns:
            bool
        """
        return self.container.make('Cache').exists(self.template)

    def __is_expired_cache(self):
        """Check if cache is expired.

        Returns:
            bool
        """
        # Check if cache_for is set and configurate
        if self.cache_time is None or self.cache_type is None and self.cache:
            return True

        driver_cache = self.container.make('Cache')

        # True is expired
        return not driver_cache.is_valid(self.template)

    def __get_cached_template(self):
        """Return the cached version of the template.

        Returns:
            self
        """
        driver_cache = self.container.make('Cache')
        self.rendered_template = driver_cache.get(self.template)
        return self

    def set_splice(self, splice):
        self._splice = splice
        return self
