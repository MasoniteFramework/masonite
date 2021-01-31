import os
import shutil
from os.path import isdir
from distutils.dir_util import copy_tree


def make_directory(directory):
    if not os.path.isfile(directory):
        if not os.path.exists(os.path.dirname(directory)):
            # Create the path to the model if it does not exist
            os.makedirs(os.path.dirname(directory))

        return True

    return False


def copy_migration(directory_file, to="databases/migrations"):
    import datetime

    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../")

    file_path = os.path.join(base_path, directory_file)
    to_folder = os.path.join(os.getcwd(), to)
    to_location = os.path.join(
        to_folder,
        datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M%S")
        + "_"
        + os.path.basename(directory_file),
    )
    # if needed
    make_directory(to_folder)
    shutil.copyfile(file_path, to_location)

    print("\033[92m {} has been created \033[0m".format(to_location))


def copy_assets(from_location, to="public", override=True):
    """Copy asset file/directory to existing directory or new directory.
    Files will be overriden."""
    # if needed
    make_directory(to)
    if isdir(from_location):
        import pdb

        pdb.set_trace()
        copy_tree(from_location, to, update=1 if override else 0)
    else:
        shutil.copy2(from_location, to)

    print("\033[92m {} has been created \033[0m".format(to))
