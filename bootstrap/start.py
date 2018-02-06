''' Start of Application. This function is the gunicorn server '''
from pydoc import locate

def app(environ, start_response):
    from wsgi import container

    '''
    |--------------------------------------------------------------------------
    | Startup the Service Container
    |--------------------------------------------------------------------------
    |
    | Instantiate the Service Container so we can bind classes into it and 
    | bind the environ variable that is created by the WSGI server into
    | the container.
    |
    '''
    
    container.bind('Environ', environ)

    '''
    |--------------------------------------------------------------------------
    | Execute All Service Providers
    |--------------------------------------------------------------------------
    |
    | Run all service provider boot methods if the wsgi attribute is true.
    |
    '''

    for provider in container.make('Application').PROVIDERS:
        located_provider = locate(provider)().load_app(container)
        if located_provider.wsgi is True:
            container.resolve(located_provider.boot)

    '''
    |--------------------------------------------------------------------------
    | We Are Ready For Launch
    |--------------------------------------------------------------------------
    |
    | If we have a solid response and not redirecting then we need to return
    | a 200 status code along with the data. If we don't, then we'll have
    | to return a 302 and redirect to where the developer would like to
    | go next.
    |
    '''

    start_response(container.make('StatusCode'), container.make('Headers'))

    '''
    |--------------------------------------------------------------------------
    | Final Step
    |--------------------------------------------------------------------------
    |
    | This will take the data variable from above and return it to the WSGI
    | server.
    |
    '''

    return iter([bytes(container.make('Response'), 'utf-8')])
