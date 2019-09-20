class Command:
    def execute(self):
        raise NotImplementedError


class LogCommand(Command):
    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self):
        self.reciever.log()


class Invoker:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def run(self):
        self.command.execute()


class Logger:
    def __init__(self, message):
        self.message = message

    def log(self):
        print(self.message)

