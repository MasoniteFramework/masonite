'''
|--------------------------------------------------------------------------
| Application Name
|--------------------------------------------------------------------------
|
| This value is the name of your application. This value is used when the
| framework needs to place the application's name in a notification or
| any other location as required by the application or its packages.
|
'''

name = 'Larapy'

'''
|--------------------------------------------------------------------------
| Application Debug Mode
|--------------------------------------------------------------------------
|
| When your application is in debug mode, detailed error messages with
| stack traces will be shown on every error that occurs within your
| application. If disabled, a simple generic error page is shown.
|
'''

debug = True

'''
|--------------------------------------------------------------------------
| Application URL
|--------------------------------------------------------------------------
|
| This URL is used by the console to properly generate URLs when using
| the Artisan command line tool. You should set this to the root of
| your application so that it is used when running Artisan tasks.
|
'''

url = 'http://localhost'

'''
|--------------------------------------------------------------------------
| Providers List
|--------------------------------------------------------------------------
|
| This providers list is used to add functionality to this project. You
| can add modules to this list which will import them when the command
| line is ran. Add modules here with function which can be picked up
| by the command line. For example: when you add a module with the 
| function 'auth' then that function will become available when
| you run: python craft vendor function_name_here
|
'''

providers = [
    'app.providers.helpers',
    'app.providers.auth',
]
