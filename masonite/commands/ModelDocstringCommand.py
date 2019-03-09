""" A ModelDocstringCommand Command """

from cleo import Command

from config.database import DB


class ModelDocstringCommand(Command):
    """
    Generate a model docstring based on a table definition

    model:docstring
        {table : Name of the table to generate the docstring for}
        {--c|connection=default : The connection to use}
    """

    def handle(self):
        if self.option('connection') == 'default':
            conn = DB.get_schema_manager().list_table_columns(self.argument('table'))
        else:
            conn = DB.connection(self.option('connection')).get_schema_manager().list_table_columns(self.argument('table'))

        docstring = '"""Model Definition (generated with love by Masonite) \n\n'
        for name, column in conn.items():
            length = '({})'.format(column._length) if column._length else ''
            docstring += '{}: {}{} default: {}\n'.format(
                name, column.get_type(), length, column.get_default())

        print(docstring + '"""')
