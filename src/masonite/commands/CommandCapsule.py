class CommandCapsule:
    def __init__(self, command_application):
        self.command_application = command_application
        self.commands = []
        self.command_name = []

    def add(self, *commands):
        for command in commands:
            command_name = command.config.name
            if command_name in self.command_name:
                continue
            self.command_name.append(command_name)
            self.commands.append(command)
            self.command_application.add_commands(command)
        return self

    def swap(self, command):
        command_name = command.config.name
        # if command with same name has been registered remove it
        if self.command_application.find(command_name):
            # no public API to do this yet
            del self.command_application.commands._commands[command_name]
        self.add(command)

    def run(self):
        return self.command_application.run()
