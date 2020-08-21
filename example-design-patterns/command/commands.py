import sys
from .command import ICommand


class ExitCommand(ICommand):
    def execute(self):
        sys.exit(0)


class LogCommand(ICommand):
    '''Log a message'''

    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self):
        self.reciever.log()


class AddCommand(ICommand):
    '''Add some numbers and return the result'''

    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self, *args):
        answer = self.reciever.add(*args)

        print(f'{" + ".join(args)} = {answer}')


class Logger:
    '''Receiver - Techincally this should implement an interface the LogCommand
    knows about, but ignoring to keep the example simple'''

    def __init__(self, message):
        self.message = message

    def log(self):
        print(self.message)


class Adder:
    '''Receiver - Techincally this should implement an interface the AddCommand
    knows about, but ignoring to keep the example simple'''

    def add(self, *args):
        return sum(int(x) for x in args)
