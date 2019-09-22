class InvalidCommandError(Exception):
    pass


# Command interface
class Command:
    def execute(self):
        raise NotImplementedError


class Invoker:
    def __init__(self):
        self.commands = {}

    def set_command(self, name, command):
        if not isinstance(command, Command):
            raise AttributeError('command must be a Command class')

        self.commands[name] = command

    def run_command(self, name):
        if name not in self.commands:
            raise InvalidCommandError(f'{name}: command not found')

        self.commands[name].execute()
