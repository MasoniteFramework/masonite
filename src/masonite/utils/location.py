"""Helpers to resolve absolute paths to the different app resources using a configured
location."""
from os.path import join, abspath

from .str import as_filepath


def _build_path(location_key, relative_path, absolute):
    from wsgi import application

    relative_dir = join(as_filepath(application.make(location_key)), relative_path)
    return abspath(relative_dir) if absolute else relative_dir


def base_path(relative_path=""):
    """Build the absolute path to the project root directory or build the absolute path to a
    given file relative to the project root directory."""
    return abspath(relative_path)


def views_path(relative_path="", absolute=True):
    """Build the absolute path to the project views directory or build the absolute path to a given
    file relative to the project views directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("views.location", relative_path, absolute)


def controllers_path(relative_path="", absolute=True):
    """Build the absolute path to the project controllers directory or build the absolute path to a given
    file relative to the project controllers directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("controllers.location", relative_path, absolute)


def mailables_path(relative_path="", absolute=True):
    """Build the absolute path to the project controllers directory or build the absolute path to a given
    file relative to the project controllers directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("mailables.location", relative_path, absolute)


def config_path(relative_path="", absolute=True):
    """Build the absolute path to the project configuration directory or build the absolute path to a given
    file relative to the project configuration directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("config.location", relative_path, absolute)


def migrations_path(relative_path="", absolute=True):
    """Build the absolute path to the project migrations directory or build the absolute path to a given
    file relative to the project migrations directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("migrations.location", relative_path, absolute)


def seeds_path(relative_path="", absolute=True):
    """Build the absolute path to the project seeds directory or build the absolute path to a given
    file relative to the project seeds directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("seeds.location", relative_path, absolute)


def jobs_path(relative_path="", absolute=True):
    """Build the absolute path to the project jobs directory or build the absolute path to a given
    file relative to the project jobs directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("jobs.location", relative_path, absolute)


def resources_path(relative_path="", absolute=True):
    """Build the absolute path to the project resources directory or build the absolute path to a given
    file relative to the project resources directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("resources.location", relative_path, absolute)


def models_path(relative_path="", absolute=True):
    """Build the absolute path to the project models directory or build the absolute path to a given
    file relative to the project models directory.

    The relative path can be returned instead by setting absolute=False."""
    return _build_path("models.location", relative_path, absolute)
