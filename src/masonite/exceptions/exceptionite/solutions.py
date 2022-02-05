class TableNotFound:
    def title(self):
        return "Table Not Found"

    def description(self):
        return "You are trying to make a query on a table that cannot be found. Check that :table migration exists and that migrations have been ran with 'python craft migrate' command."

    def regex(self):
        return r"no such table: (?P<table>(\w+))"
