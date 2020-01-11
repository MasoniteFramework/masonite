"""New Authentication System Command."""
import os
import shutil

from cleo import Command
from ..helpers.filesystem import make_directory


class AuthCommand(Command):
    """
    Creates an authentication system.

    auth
    """

    def handle(self):
        self.info('Scaffolding Application ...')
        module_path = os.path.dirname(os.path.realpath(__file__))

        with open('routes/web.py', 'a') as f:
            # add all the routes
            f.write("\nfrom masonite.auth import Auth \n")
            f.write("ROUTES += Auth.routes()")
            f.write('\n')

        make_directory(os.path.join(os.getcwd(), 'app/http/controllers/auth/LoginController.py'))

        # move controllers
        shutil.copyfile(module_path + "/../snippets/auth/controllers/LoginController.py",
                        os.getcwd() + "/app/http/controllers/auth/LoginController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/RegisterController.py",
                        os.getcwd() + "/app/http/controllers/auth/RegisterController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/HomeController.py",
                        os.getcwd() + "/app/http/controllers/auth/HomeController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/ConfirmController.py",
                        os.getcwd() + "/app/http/controllers/auth/ConfirmController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/PasswordController.py",
                        os.getcwd() + "/app/http/controllers/auth/PasswordController.py")
        # move templates
        shutil.copytree(module_path + "/../snippets/auth/templates/auth",
                        os.getcwd() + "/resources/templates/auth")

        self.info('Project Scaffolded. You now have 5 new controllers, 7 new templates and 9 new routes')
