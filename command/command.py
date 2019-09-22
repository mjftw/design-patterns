import sys

# Command interface
class Command:
    def execute(self):
        raise NotImplementedError


# Concerete Command implimenting Command interface
class LogCommand(Command):
    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self):
        self.reciever.log()



class InvalidCommandError(Exception):
    pass


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


class ExitCommand(Command):
    def execute(self):
        sys.exit()


class CommandLineInterface(Invoker):
    def __init__(self):
        Invoker.__init__(self)

        self.set_command('exit', ExitCommand())

    def run(self):
        while True:
            try:
                cmd = input('cli$ ')
                self.run_command(cmd)
            except EOFError:
                self.run_command('exit')
            except InvalidCommandError as e:
                print(str(e))


# Reciever
class Logger:
    def __init__(self, message):
        self.message = message

    def log(self):
        print(self.message)
