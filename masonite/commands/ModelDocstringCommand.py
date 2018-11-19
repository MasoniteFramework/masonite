""" A ModelDocstringCommand Command """

from cleo import Command

from config.database import DB


class ModelDocstringCommand(Command):
    """
    Generate a model docstring based on a table definition

    model:docstring
        {table : Name of the table to generate the docstring for}
    """

    def handle(self):
        conn = DB.get_schema_manager().list_table_columns(self.argument('table'))
        docstring = '"""Model Definition (generated with love by Masonite) \n\n'
        for name, column in conn.items():
            length = '({})'.format(column._length) if column._length else ''
            docstring += '{}: {}{} default: {}\n'.format(
                name, column.get_type(), length, column.get_default())

        print(docstring + '"""')
