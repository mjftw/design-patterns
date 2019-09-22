
from command import Command
from cli import CLI


# Concerete Class implimenting Command interface
class LogCommand(Command):
    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self):
        self.reciever.log()


# Reciever
class Logger:
    def __init__(self, message):
        self.message = message

    def log(self):
        print(self.message)
