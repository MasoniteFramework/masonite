from subprocess import call
from cleo import Command


class ServeCommand(Command):
    """
    Run the Masonite server

    serve
        {--port=8000 : Specify which port to run the server}
        {--host=127.0.0.1 : Specify which ip address to run the server}
    """

    def handle(self):
        try:
            call([
                "waitress-serve", '--port', self.option('port'),
                "--host", self.option('host'), "wsgi:application"
            ])
        except Exception:
            self.line('')
            self.comment('Server aborted!')
