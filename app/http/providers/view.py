import re
from jinja2 import Template
from jinja2 import Environment, PackageLoader, select_autoescape


def view(template = 'index', dictionary = {}):
    file = open('./resources/templates/'+ template + '.blade.html', 'r')
    env = Environment(
        loader=PackageLoader('resources', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    return env.get_template(template + '.blade.html').render()

    # Blade Template Engine
    # file = file.read()
    # file = re.sub(r'(\s*)@if(\s*\(.*\))', r'{% if \2 %}', file)
    # file = re.sub(r'@endif', r'{% endif %}', file)
    # file = re.sub(r'@else', r'{% else %}', file)

    
    # template = Template(file)
    # return template.render(dictionary)
