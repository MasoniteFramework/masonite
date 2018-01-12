''' Third party package integrations '''
import os
import sys
import shutil

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
        ## Append to the file
        # tempfiles is a list of file handles to your temp files. Order them however you like
        project_config = open(config_directory + '/' + file_name, "a")
        package_config = open(location, 'r')

        project_config.write(package_config.read())

        project_config.close()
        package_config.close()
        print('\033[92mConfiguration File Appended!\033[0m')


def append_web_routes(location):
    # import it into the web.py file
    routes_file = os.path.join(os.getcwd(), 'routes/web.py')

    ## Append to the file
    # tempfiles is a list of file handles to your temp files. Order them however you like
    project_routes = open(routes_file, "a")
    package_routes = open(location, 'r')

    project_routes.write(package_routes.read())

    project_routes.close()
    package_routes.close()
    print('\033[92mroutes/web.py File Appended!\033[0m')

def append_api_routes(location):
    # import it into the web.py file
    api_file = os.path.join(os.getcwd(), 'routes/api.py')

    ## Append to the file
    # tempfiles is a list of file handles to your temp files. Order them however you like
    project_routes = open(api_file, "a")
    package_routes = open(location, 'r')

    project_routes.write(package_routes.read())

    project_routes.close()
    package_routes.close()
    print('\033[92mroutes/api.py File Appended!\033[0m')


def create_controller(location):
    file_name = os.path.basename(location)

    controller_directory = os.path.join(os.getcwd(), 'app/http/controllers')
    controller_file = os.path.join(controller_directory, file_name)

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
