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
import os

NAME = 'Masonite'

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

DEBUG = True

'''
|--------------------------------------------------------------------------
| Secret Key
|--------------------------------------------------------------------------
|
| This key is used to encrypt and decrypt various values. Out of the box
| Masonite uses this key to encrypt and decrypt cookies but you can use
| it to encrypt and decrypt various values using the Masonite Sign
| class. Read the documentation on Encryption to find out how.
|
'''

KEY = os.environ.get('key')

'''
|--------------------------------------------------------------------------
| Application URL
|--------------------------------------------------------------------------
|
| Currently not in use. Will add documentation at a later date
|
'''

URL = 'http://localhost'

'''
|--------------------------------------------------------------------------
| Providers List
|--------------------------------------------------------------------------
|
| This providers list is used to add functionality to this project. You
| can add modules to this list which will import them when the command
| line is ran. Add modules here with a function which can be picked up
| by the command line. For example: when you add a module with the
| function 'auth' then that function will become available when
| you run: python craft auth
|
'''

PROVIDERS = []

'''
|--------------------------------------------------------------------------
| Base Directory
|--------------------------------------------------------------------------
|
| TODO
|
'''

BASE_DIRECTORY = os.getcwd()

'''
|--------------------------------------------------------------------------
| Static Root
|--------------------------------------------------------------------------
|
| TODO
|
'''

STATIC_ROOT = os.path.join(BASE_DIRECTORY, 'storage')
