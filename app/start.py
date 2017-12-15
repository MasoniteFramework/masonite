import os
import re
from app.http.providers.routes import Route
from app.http.providers.request import Request
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def app(environ, start_response):
    ''' Framework Engine '''
    os.environ.setdefault('REQUEST_METHOD', environ['REQUEST_METHOD'])
    os.environ.setdefault('URI_PATH', environ['PATH_INFO'])

    # if this is a post request
    if environ['REQUEST_METHOD'] == 'POST':
        l = int(environ.get('CONTENT_LENGTH')) if environ.get(
            'CONTENT_LENGTH') else 0
        body = environ['wsgi.input'].read(l) if l > 0 else ''
        environ['QUERY_STRING'] = body

    router = Route(environ)
    import routes.web
    routes = routes.web.routes
    request = Request(environ)

    for route in routes:
        split_given_route = route.route.split('/')

        url_list = []
        regex = '^'
        for regex_route in split_given_route:
            if '@' in regex_route:
                if ':int' in regex_route:
                    regex += '(\d+)'
                elif ':string' in regex_route:
                    regex += '([a-zA-Z]+)'
                else:
                    # default
                    regex += '(\w+)'
                regex += '\/'

                # append the variable name passed @(variable):int to a list
                url_list.append(
                    regex_route.replace('@', '').replace(':int', '').replace(':string', '')
                )
            else:
                regex += regex_route + '\/'

        regex += '$'
        if route.route.endswith('/'):
            matchurl = re.compile(regex.replace('\/\/$', '\/$'))
        else:
            matchurl = re.compile(regex.replace('\/$', '$'))

        try:
            parameter_dict = {}
            for index, value in enumerate(matchurl.match(router.url).groups()):
                parameter_dict[url_list[index]] = value
            request.set_params(parameter_dict)
        except AttributeError:
            pass


        print request.url_params

        if matchurl.match(router.url) and route.method_type == environ['REQUEST_METHOD'] and route.continueroute is True:
            print route.method_type + ' Route: ' + router.url
            data = router.get(route.route, route.output(request))
            break
        else:
            data = 'Route not found. Error 404'

    if data == 'Route not found. Error 404':
        # look at the API routes files
        import routes.api
        routes = routes.api.routes

        for route in routes:
            if route.url in router.url:
                data = route.fetch(request).output
                if data:
                    break
                else:
                    data = 'Route not found. Error 404'
            else:
                data = 'Route not found. Error 404'

    data = bytes(data)

    start_response("200 OK", [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])
