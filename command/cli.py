import sys

from command import Command, Invoker, InvalidCommandError


class ExitCommand(Command):
    def execute(self):
        sys.exit(0)


class CLI(Invoker):
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

