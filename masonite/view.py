from jinja2 import Template
from jinja2 import Environment, PackageLoader, select_autoescape


def view(template = 'index', dictionary = {}):
    env = Environment(
        loader=PackageLoader('resources', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    return env.get_template(template + '.html').render(dictionary)

class View(object):

    def __init__(self):
        self.dictionary = {}
        self.composers = {}
        self.env = Environment(
            loader=PackageLoader('resources', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, template, dictionary = {}):
        self.dictionary.update(dictionary)
        
        if template in self.composers:
            self.dictionary.update(self.composers[template])
        
        if '*' in self.composers:
            self.dictionary.update(self.composers['*'])

        return self.env.get_template(template + '.html').render(self.dictionary)
    
    def composer(self, composer_name, dictionary):

        if isinstance(composer_name, str):
            self.composers[composer_name] = dictionary

        if isinstance(composer_name, list):
            for composer in composer_name:
                self.composers[composer] = dictionary

        return self

    def extend(self):
        pass
    
    def share(self, dictionary):
        self.dictionary.update(dictionary)
        return self
