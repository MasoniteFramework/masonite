""" An ApiProvider Service Provider """
from masonite.provider import ServiceProvider


class ApiProvider(ServiceProvider):

    def register(self):
        pass

    def boot(self, Response, ApiRoutes, Route, Request):
        router = Route
        if Response == 'Route not found. Error 404':

            """
            |--------------------------------------------------------------------------
            | Pull in the API Routes from the Service Container
            |--------------------------------------------------------------------------
            |
            | The Service Container has loaded all Api routes into the container so
            | let's loop through and check for any matches.
            |
            """

            for route in ApiRoutes:

                """
                |--------------------------------------------------------------------------
                | If We've Got A Match
                |--------------------------------------------------------------------------
                |
                | If we have a match then let's go ahead and execute the route, load the 
                | response into the data variable and get on with our lives.
                |
                """

                if route.url in router.url:
                    data = route.fetch(Request).output
                    if data:
                        break
                    else:
                        data = 'Route not found. Error 404'
                else:
                    data = 'Route not found. Error 404'
