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
            f.write("Get().route('/login', 'auth.LoginController@show').name('login'),\n    ")
            f.write("Get().route('/logout', 'auth.LoginController@logout').name('logout'),\n    ")
            f.write("Post().route('/login', 'auth.LoginController@store'),\n    ")
            f.write("Get().route('/register', 'auth.RegisterController@show').name('register'),\n    ")
            f.write("Post().route('/register', 'auth.RegisterController@store'),\n    ")
            f.write("Get().route('/home', 'auth.HomeController@show').name('home'),\n    ")
            f.write("Get().route('/email/verify', 'auth.ConfirmController@verify_show').name('verify'),\n    ")
            f.write("Get().route('/email/verify/@id:signed', 'auth.ConfirmController@confirm_email'),\n    ")
            f.write("Get().route('/email/verify/@id:signed', 'auth.ConfirmController@confirm_email'),\n    ")
            f.write("Get().route('/password', 'auth.PasswordController@forget').name('forgot.password'),\n    ")
            f.write("Post().route('/password', 'auth.PasswordController@send'),\n    ")
            f.write("Get().route('/password/@token/reset', 'auth.PasswordController@reset').name('password.reset'),\n    ")
            f.write("Post().route('/password/@token/reset', 'auth.PasswordController@update'),\n")
            f.write(']\n')

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
