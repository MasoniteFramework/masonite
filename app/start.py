''' Start of Application. This function is the gunicorn server '''

import os
import re

import sass
from dotenv import find_dotenv, load_dotenv
from masonite.request import Request
from masonite.routes import Route

from config import application, storage

load_dotenv(find_dotenv())

matches = []

for files in storage.SASSFILES['importFrom']:
    for root, dirnames, filenames in os.walk(os.path.join(application.BASE_DIRECTORY, files)):
        for filename in filenames:
            if filename.endswith(('.sass', '.scss')) and not filename.startswith('_'):
                matches.append(os.path.join(root, filename))

for filename in matches:
    with open(filename) as f:
        compiled_sass = sass.compile(string=f.read(), include_paths=storage.SASSFILES['includePaths'])
        name = filename.split('/')[-1].replace('.scss', '').replace('.sass', '')
    write_file = os.path.join(application.BASE_DIRECTORY, storage.SASSFILES['compileTo'] + '/{0}.css'.format(name))
    with open(write_file, 'w') as r:
        r.write(compiled_sass)

def app(environ, start_response):
    ''' Framework Engine '''
    os.environ.setdefault('REQUEST_METHOD', environ['REQUEST_METHOD'])
    os.environ.setdefault('URI_PATH', environ['PATH_INFO'])

    # if this is a post request
    if environ['REQUEST_METHOD'] == 'POST':
        get_post_params = int(environ.get('CONTENT_LENGTH')) if environ.get(
            'CONTENT_LENGTH') else 0
        body = environ['wsgi.input'].read(get_post_params) if get_post_params > 0 else ''
        environ['QUERY_STRING'] = body.decode('utf-8')

    router = Route(environ)
    import routes.web
    routes = routes.web.ROUTES
    request = Request(environ)

    for route in routes:
        split_given_route = route.route_url.split('/')

        url_list = []
        regex = '^'
        for regex_route in split_given_route:
            if '@' in regex_route:
                if ':int' in regex_route:
                    regex += r'(\d+)'
                elif ':string' in regex_route:
                    regex += r'([a-zA-Z]+)'
                else:
                    # default
                    regex += r'(\w+)'
                regex += r'\/'

                # append the variable name passed @(variable):int to a list
                url_list.append(
                    regex_route.replace('@', '').replace(':int', '').replace(':string', '')
                )
            else:
                regex += regex_route + r'\/'

        regex += '$'
        if route.route_url.endswith('/'):
            matchurl = re.compile(regex.replace(r'\/\/$', r'\/$'))
        else:
            matchurl = re.compile(regex.replace(r'\/$', r'$'))

        try:
            parameter_dict = {}
            for index, value in enumerate(matchurl.match(router.url).groups()):
                parameter_dict[url_list[index]] = value
            request.set_params(parameter_dict)
        except AttributeError:
            pass

        if matchurl.match(router.url) and route.method_type == environ['REQUEST_METHOD'] and route.continueroute is True:
            print(route.method_type + ' Route: ' + router.url)
            data = router.get(route.route, route.output(request))
            break
        else:
            data = 'Route not found. Error 404'

    if data == 'Route not found. Error 404':
        # look at the API routes files
        import routes.api
        routes = routes.api.ROUTES

        for route in routes:
            if route.url in router.url:
                data = route.fetch(request).output
                if data:
                    break
                else:
                    data = 'Route not found. Error 404'
            else:
                data = 'Route not found. Error 404'

    if request.redirect_route:
        for route in routes:
            if route.named_route == request.redirect_route:
                print(route.method_type + ' Named Route: ' + router.url)
                data = router.get(route.route, route.output(request))
                request.redirect_url = route.route_url


    data = bytes(data, 'utf-8')

    if not request.redirect_url:
        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(data)))
        ] + request.get_cookies())
    else:
        start_response("302 OK", [
            ('Location', request.redirect_url)
        ] + request.get_cookies())

    return iter([data])
