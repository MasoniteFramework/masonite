"""New Authentication System Command."""
import os
import shutil

from cleo import Command


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
            f.write('\nROUTES = ROUTES + [\n    ')
            f.write("Get().route('/login', 'LoginController@show').name('login'),\n    ")
            f.write("Get().route('/logout', 'LoginController@logout').name('logout'),\n    ")
            f.write("Post().route('/login', 'LoginController@store'),\n    ")
            f.write("Get().route('/register', 'RegisterController@show').name('register'),\n    ")
            f.write("Post().route('/register', 'RegisterController@store'),\n    ")
            f.write("Get().route('/home', 'HomeController@show').name('home'),\n    ")
            f.write("Get().route('/email/verify', 'ConfirmController@verify_show').name('verify'),\n    ")
            f.write("Get().route('/email/verify/@id:signed', 'ConfirmController@confirm_email'),\n    ")
            f.write("Get().route('/email/verify/@id:signed', 'ConfirmController@confirm_email'),\n    ")
            f.write("Get().route('/password', 'PasswordController@forget').name('forgot.password'),\n    ")
            f.write("Post().route('/password', 'PasswordController@send'),\n    ")
            f.write("Get().route('/password/@token/reset', 'PasswordController@reset').name('password.reset'),\n    ")
            f.write("Post().route('/password/@token/reset', 'PasswordController@update'),\n")
            f.write(']\n')

        # move controllers
        shutil.copyfile(module_path + "/../snippets/auth/controllers/LoginController.py",
                        os.getcwd() + "/app/http/controllers/LoginController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/RegisterController.py",
                        os.getcwd() + "/app/http/controllers/RegisterController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/HomeController.py",
                        os.getcwd() + "/app/http/controllers/HomeController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/ConfirmController.py",
                        os.getcwd() + "/app/http/controllers/ConfirmController.py")
        shutil.copyfile(module_path + "/../snippets/auth/controllers/PasswordController.py",
                        os.getcwd() + "/app/http/controllers/PasswordController.py")
        # move templates
        shutil.copytree(module_path + "/../snippets/auth/templates/auth",
                        os.getcwd() + "/resources/templates/auth")

        self.info('Project Scaffolded. You now have 5 new controllers, 7 new templates and 9 new routes')
