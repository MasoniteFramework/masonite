import re
from jinja2 import Template

def view(template = 'index', dictionary = {}):
    print(dictionary)
    # /(\s*)@if(\s*\(.*\))/

    file = open('./resources/templates/'+ template + '.blade.html', 'r')
    file = file.read()
    file = re.sub(r'(\s*)@if(\s*\(.*\))', r'{% if \2 %}', file)
    file = re.sub(r'@endif', r'{% endif %}', file)
    file = re.sub(r'@else', r'{% else %}', file)
    template = Template(file)
    return template.render(dictionary)