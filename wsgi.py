from masonite.app import App
from bootstrap.start import app
from config import application
from pydoc import locate
from dotenv import find_dotenv, load_dotenv

'''
|--------------------------------------------------------------------------
| Load Environment Variables
|--------------------------------------------------------------------------
|
| Take environment variables from the .env file and load them in.
|
'''

load_dotenv(find_dotenv())

'''
|--------------------------------------------------------------------------
| Instantiate Container And Perform Important Bindings
|--------------------------------------------------------------------------
|
| Some Service providers need important bindings like the WSGI application
| and the application configuration file before they boot.
|
'''

container = App()

container.bind('WSGI', app)
container.bind('Application', application)

'''
|--------------------------------------------------------------------------
| Bind all service providers
|--------------------------------------------------------------------------
|
| Let's register everything into the Service Container. Once everything is
| in the container we can run through all the boot methods. For reasons
| some providers don't need to execute with every request and should
| only run once when the server is started. Providers will be ran
| once if the wsgi attribute on a provider is False.
|
'''

for provider in container.make('Application').PROVIDERS:
    locate(provider)().load_app(container).register()

for provider in container.make('Application').PROVIDERS:
    located_provider = locate(provider)().load_app(container)

    if located_provider.wsgi is False:
        container.resolve(locate(provider)().load_app(container).boot)

'''
|--------------------------------------------------------------------------
| Get the application from the container
|--------------------------------------------------------------------------
|
| Some providers may change the WSGI Server like wrapping the WSGI server
| in a Whitenoise container for an example. Let's get a WSGI instance
| from the container and pass it to the application variable. This
| will allow WSGI servers to pick it up from the command line
|
'''

application = container.make('WSGI')
