"""Third party package integrations."""
import os
import shutil
import sys


def create_or_append_config(location, name=False):
    if name:
        file_name = name
    else:
        file_name = os.path.basename(location)

    # import it into the config directory
    config_directory = os.path.join(os.getcwd(), 'config')

    # if file does not exist
    if not os.path.isfile(config_directory + '/' + file_name):
        shutil.copyfile(location,
                        config_directory + '/' + file_name)
        print('\033[92mConfiguration File Created!\033[0m')
    else:
        # Append to the file
        # tempfiles is a list of file handles to your temp files.
        project_config = open(config_directory + '/' + file_name, "a")
        package_config = open(location, 'r')

        project_config.write(package_config.read())

        project_config.close()
        package_config.close()
        print('\033[92mConfiguration File Appended!\033[0m')


def append_web_routes(location):
    # import it into the web.py file
    routes_file = os.path.join(os.getcwd(), 'routes/web.py')

    # Append to the file
    # tempfiles is a list of file handles to your temp files.
    project_routes = open(routes_file, "a")
    package_routes = open(location, 'r')

    project_routes.write(package_routes.read())

    project_routes.close()
    package_routes.close()
    print('\033[92mroutes/web.py File Appended!\033[0m')


def append_api_routes(location):
    # import it into the web.py file
    api_file = os.path.join(os.getcwd(), 'routes/api.py')

    # Append to the file
    # tempfiles is a list of file handles to your temp files.
    project_routes = open(api_file, "a")
    package_routes = open(location, 'r')

    project_routes.write(package_routes.read())

    project_routes.close()
    package_routes.close()
    print('\033[92mroutes/api.py File Appended!\033[0m')


def create_controller(location, to='app/http/controllers'):
    file_name = os.path.basename(location)

    controller_directory = os.path.join(os.getcwd(), to)
    controller_file = os.path.join(controller_directory, file_name)
    if not os.path.exists(controller_directory):
        # Create the path to the model if it does not exist
        os.makedirs(controller_directory)

    if os.path.isfile(controller_file):
        # if file does exist
        print('\033[91m{0} Controller Already Exists!\033[0m'.format(file_name))
    else:
        # copy controller over
        shutil.copyfile(
            location,
            controller_file
        )

        print('\033[92m{0} Controller Created\033[0m'.format(file_name))


def add_venv_site_packages():
    try:
        from config import packages
        # Add additional site packages to vendor if they exist
        for directory in packages.SITE_PACKAGES:
            path = os.path.join(os.getcwd(), directory)
            sys.path.append(path)
    except ImportError:
        raise ImportError

    if 'VIRTUAL_ENV' in os.environ:
        python_version = None
        venv_directory = os.listdir(
            os.path.join(os.environ['VIRTUAL_ENV'], 'lib')
        )

        for directory in venv_directory:
            if directory.startswith('python'):
                python_version = directory
                break

        if python_version:
            site_packages_directory = os.path.join(
                os.environ['VIRTUAL_ENV'],
                'lib',
                python_version,
                'site-packages'
            )

            sys.path.append(site_packages_directory)
        else:
            print('\033[93mWARNING: Could not add the virtual environment you are currently in. Attempting to add: {0}\033[93m'.format(
                os.environ['VIRTUAL_ENV']))
