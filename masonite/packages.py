''' Third party package integrations '''
import os
import sys
import shutil

def create_or_append_config(location, name=False):
    module_path = os.path.dirname(os.path.realpath(sys.argv[0]))

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
