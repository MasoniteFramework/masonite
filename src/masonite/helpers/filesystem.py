import os
import shutil


def make_directory(directory):
    if not os.path.isfile(directory):
        if not os.path.exists(os.path.dirname(directory)):
            # Create the path to the model if it does not exist
            os.makedirs(os.path.dirname(directory))

        return True

    return False


def copy_migration(directory_file, to='databases/migrations'):
    import datetime
    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../')

    file_path = os.path.join(base_path, directory_file)
    to_location = os.path.join(os.getcwd(), to, datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M%S") + '_' + os.path.basename(directory_file))
    shutil.copyfile(file_path, to_location)

    print('\033[92m {} has been created \033[0m'.format(to_location))
