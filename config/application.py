import os

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

NAME = 'Masonite'

'''
|--------------------------------------------------------------------------
| Application Debug Mode
|--------------------------------------------------------------------------
|
| When your application is in debug mode, detailed error messages with
| stack traces will be shown on every error that occurs within your
| application. If disabled, a simple generic error page is shown
|
'''

DEBUG = True

'''
|--------------------------------------------------------------------------
| Secret Key
|--------------------------------------------------------------------------
|
| This key is used to encrypt and decrypt various values. Out of the box
| Masonite uses this key to encrypt or decrypt cookies so you can use
| it to encrypt and decrypt various values using the Masonite Sign
| class. Read the documentation on Encryption to find out how.
|
'''

KEY = os.environ.get('KEY')

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
| Providers are a simple way to remove or add functionality for Masonite
| The providers in this list are either ran on server start or when a
| request is made depending on the provider. Take some time to can
| learn more more about Service Providers in our documentation
|
'''

PROVIDERS = [
    # Framework Providers
    'masonite.providers.AppProvider.AppProvider',
    'masonite.providers.RouteProvider.RouteProvider',
    'masonite.providers.ApiProvider.ApiProvider',
    'masonite.providers.RedirectionProvider.RedirectionProvider',
    'masonite.providers.StartResponseProvider.StartResponseProvider',
    'masonite.providers.SassProvider.SassProvider',
    'masonite.providers.WhitenoiseProvider.WhitenoiseProvider',
    'masonite.providers.MailProvider.MailProvider',
    'masonite.providers.UploadProvider.UploadProvider',

    # Third Party Providers

    # Application Providers
    'app.providers.UserModelProvider.UserModelProvider',
    'app.providers.MiddlewareProvider.MiddlewareProvider',
]

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
| Set the static root of your application that you wil use to store assets
|
'''

STATIC_ROOT = os.path.join(BASE_DIRECTORY, 'storage')
