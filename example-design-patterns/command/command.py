import abc


class InvalidCommandError(Exception):
    pass


class ICommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, *args):
        pass


class MacroCommand(ICommand):
    def __init__(self, *commands):
        assert all(isinstance(cmd, ICommand) for cmd in commands)

        self.commands = commands

    def execute(self, *args):
        for cmd in self.commands:
            cmd.execute()


class Invoker:
    def __init__(self):
        self.commands = {}

    def set_command(self, name: str, command: ICommand):
        if not isinstance(command, ICommand):
            raise AttributeError('command must be a ICommand class')

        self.commands[name] = command

    def run_command(self, name: str, *args):
        if name not in self.commands:
            raise InvalidCommandError(f'{name}: command not found')

        if args:
            self.commands[name].execute(*args)
        else:
            self.commands[name].execute()
