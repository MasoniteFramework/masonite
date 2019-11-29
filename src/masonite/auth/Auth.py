"""Authentication Class."""


class Auth:
    """Facade class for the Guard class"""

    @staticmethod
    def routes():
        from ..routes import Get, Post
        return [
            Get().route('/login', 'auth.LoginController@show').name('login'),
            Get().route('/logout', 'auth.LoginController@logout').name('logout'),
            Post().route('/login', 'auth.LoginController@store'),
            Get().route('/register', 'auth.RegisterController@show').name('register'),
            Post().route('/register', 'auth.RegisterController@store'),
            Get().route('/home', 'auth.HomeController@show').name('home'),
            Get().route('/email/verify', 'auth.ConfirmController@verify_show').name('verify'),
            Get().route('/email/verify/@id:signed', 'auth.ConfirmController@confirm_email'),
            Get().route('/email/verify/@id:signed', 'auth.ConfirmController@confirm_email'),
            Get().route('/password', 'auth.PasswordController@forget').name('forgot.password'),
            Post().route('/password', 'auth.PasswordController@send'),
            Get().route('/password/@token/reset', 'auth.PasswordController@reset').name('password.reset'),
            Post().route('/password/@token/reset', 'auth.PasswordController@update'),
        ]
