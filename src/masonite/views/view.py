"""View Module."""
from collections import defaultdict
from os.path import split, exists
from jinja2 import ChoiceLoader, Environment, PackageLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound

from ..exceptions import ViewException
from ..utils.str import as_filepath
from ..utils.location import views_path


def path_to_package(path, separator="/"):
    # ensure no leading/trailing slashes before splitting to avoid blank strings
    location = path.strip(separator).split(separator)
    package_name = location[0]
    package_path = "/".join(location[1:])
    return package_name, package_path


class View:
    """Responsible for handling everything involved with views and view environments."""

    separator = "/"
    extension = ".html"

    def __init__(self, application):
        self.application = application

        # specific to given view rendering
        self.dictionary = {}
        self.composers = {}
        self.template = None
        self.loaders = []
        self.namespaces = defaultdict(list)
        self.env = None
        self._jinja_extensions = ["jinja2.ext.loopcontrols"]
        self._filters = {}
        self._shared = {}
        self._tests = {}

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
            raise ViewException(
                "Second parameter to render method needs to be a dictionary, {} passed.".format(
                    type(dictionary).__name__
                )
            )

        self.load_template(template)

        # prepare template context
        self.dictionary = {}
        self.dictionary.update(dictionary)
        self.dictionary.update(self._shared)
        if self.composers:
            self.hydrate_from_composers()

        if self._tests:
            self.env.tests.update(self._tests)

        self.rendered_template = self._render()

        return self

    def get_content(self):
        return self.rendered_template

    def _render(self):
        try:
            # Try rendering the template with '.html' appended
            return self.env.get_template(self.filename).render(self.dictionary)
        except TemplateNotFound:
            # Try rendering the direct template the user has supplied
            return self.env.get_template(self.template).render(self.dictionary)

    def hydrate_from_composers(self):
        """Add data into the view from specified composers."""
        # Check if the template is directly specified in the composer
        if self.template in self.composers:
            self.dictionary.update(self.composers.get(self.template))

        # Check if there is just an astericks in the composer
        if "*" in self.composers:
            self.dictionary.update(self.composers.get("*"))

        # We will append onto this string for an easier way to search through wildcard routes
        compiled_string = ""

        # Check for wildcard view composers
        for template in self.template.split(self.separator):
            # Append the template onto the compiled_string
            compiled_string += template
            if self.composers.get("{}*".format(compiled_string)):
                self.dictionary.update(self.composers["{}*".format(compiled_string)])
            else:
                # Add a slash to symbolize going into a deeper directory structure
                compiled_string += "/"

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

    def exists(self, template):
        """Check if a template exists.

        Arguments:
            template {string} -- Name of the template to check for.

        Returns:
            bool
        """
        self.load_template(template)

        try:
            self.env.get_template(self.filename)
            return True
        except TemplateNotFound:
            return False

    def add_location(self, template_location, loader=PackageLoader):
        """Add locations from which view templates can be loaded.

        Arguments:
            template_location {str} -- Directory location

        Keyword Arguments:
            loader {jinja2.Loader} -- Type of Jinja2 loader to use. (default: {jinja2.PackageLoader})
        """
        if loader == PackageLoader:
            package_name, package_path = path_to_package(template_location)
            self.loaders.append(loader(package_name, package_path))
        else:
            self.loaders.append(loader(template_location))

    def add_namespaced_location(self, namespace, template_location):
        # if views have been published, add the published view directory as a location
        published_path = views_path(f"vendor/{namespace}/", absolute=False)
        if exists(published_path):
            self.namespaces[namespace].append(
                views_path(f"vendor/{namespace}/", absolute=False)
            )
        # put this one in 2nd as project views must be used first to be able to override package views
        self.namespaces[namespace].append(template_location)

    def add_from_package(self, package_name, path_in_package):
        self.environments.append(PackageLoader(package_name, path_in_package))

    def add_namespace(self, namespace, path):
        # TODO: if views have been published, add an other path corresponding to this namespace
        self.namespaces[namespace].append(
            views_path(f"vendor/{namespace}/", absolute=False)
        )
        # put this one in 2nd as project (overriden) views must be used first
        self.namespaces[namespace].append(path)

    def filter(self, name, function):
        """Use to add filters to views.

        Arguments:
            name {string} -- Key to bind the filter to.
            function {object} -- Function used for the template filter.
        """
        self._filters.update({name: function})

    def add_extension(self, extension):
        self._jinja_extensions.append(extension)
        return self

    def load_template(self, template):
        """Private method for loading all the locations into the current environment.

        Arguments:
            template {string} -- Template to load environment from.
        """
        self.template = template
        # transform given template path into a real file path with the configured extension
        self.filename = (
            as_filepath(template).replace(self.extension, "") + self.extension
        )
        # assess if new loaders are required for the given template
        template_loaders = []
        # Case 1: the templates needs to be loaded from a namespace
        if ":" in template:
            namespace, rel_template_path = template.split(":")
            self.filename = (
                as_filepath(rel_template_path).replace(self.extension, "")
                + self.extension
            )
            namespace_paths = self.namespaces.get(namespace, None)
            if not namespace_paths:
                raise Exception(f"No such view namespace {namespace}.")
            for namespace_path in namespace_paths:
                package_name, package_path = path_to_package(namespace_path)
                template_loaders.append(PackageLoader(package_name, package_path))

        # Case 2: an absolute path has been given
        elif template.startswith("/"):
            directory, filename = split(template)
            self.filename = filename.replace(self.extension, "") + self.extension
            package_name, package_path = path_to_package(directory)
            template_loaders.append(PackageLoader(package_name, package_path))

        # Else: use already defined view locations to load this template
        loader = ChoiceLoader(template_loaders + self.loaders)

        # @josephmancuso: what is this ??
        # Set the searchpath since some packages look for this object
        # This is sort of a hack for now
        loader.searchpath = ""

        self.env = Environment(
            loader=loader,
            autoescape=select_autoescape(["html", "xml"]),
            extensions=self._jinja_extensions,
            line_statement_prefix="@",
        )
        # add filters to environment
        self.env.filters.update(self._filters)

    def get_current_loaders(self):
        if self.env:
            return self.env.loader.loaders

    def set_separator(self, token):
        self.separator = token
        return self

    def set_file_extension(self, extension):
        self.extension = extension
        return self

    def get_response(self):
        return self.rendered_template

    def test(self, key, obj):
        self._tests.update({key: obj})
        return self
