"""Authentication Class."""


class Auth:
    """Facade class for the Guard class"""

    @staticmethod
    def routes():
        from ..routes import Get, Post
        return [
            Get('/login', 'auth.LoginController@show').name('login'),
            Get('/logout', 'auth.LoginController@logout').name('logout'),
            Post('/login', 'auth.LoginController@store'),
            Get('/register', 'auth.RegisterController@show').name('register'),
            Post('/register', 'auth.RegisterController@store'),
            Get('/home', 'auth.HomeController@show').name('home'),
            Get('/email/verify', 'auth.ConfirmController@verify_show').name('verify'),
            Get('/email/verify/@id:signed', 'auth.ConfirmController@confirm_email'),
            Get('/email/verify/@id:signed', 'auth.ConfirmController@confirm_email'),
            Get('/password', 'auth.PasswordController@forget').name('forgot.password'),
            Post('/password', 'auth.PasswordController@send'),
            Get('/password/@token/reset', 'auth.PasswordController@reset').name('password.reset'),
            Post('/password/@token/reset', 'auth.PasswordController@update'),
        ]
