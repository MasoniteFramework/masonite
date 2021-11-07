class CommandCapsule:
    def __init__(self, command_application):
        self.command_application = command_application
        self.commands = []

    def add(self, *commands):
        self.commands.append(commands)
        self.command_application.add_commands(*commands)
        return self

    def run(self):
        return self.command_application.run()
