from jinja2 import Template
from jinja2 import Environment, PackageLoader, select_autoescape


def view(template = 'index', dictionary = {}):
    env = Environment(
        loader=PackageLoader('resources', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    return env.get_template(template + '.html').render(dictionary)
