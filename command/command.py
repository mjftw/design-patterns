class InvalidCommandError(Exception):
    pass


# Command interface
class Command:
    def execute(self):
        raise NotImplementedError


class MacroCommand(Command):
    def __init__(self, *commands):
        assert all(isinstance(cmd, Command) for cmd in commands)

        self.commmands = commands

    def execute(self):
        for cmd in self.commmands:
            cmd.execute()


class Invoker:
    def __init__(self):
        self.commands = {}

    def set_command(self, name, command):
        if not isinstance(command, Command):
            raise AttributeError('command must be a Command class')

        self.commands[name] = command

    def run_command(self, name, *args):
        if name not in self.commands:
            raise InvalidCommandError(f'{name}: command not found')

        if args:
            self.commands[name].execute(*args)
        else:
            self.commands[name].execute()
