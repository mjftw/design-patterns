
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


def main():
    logHello = Logger('Hello World!')
    logGoodbye = Logger('Goodbye World!')

    helloCommand = LogCommand(logHello)
    goodbyeCommand = LogCommand(logGoodbye)

    cli = CLI()
    cli.set_command('hello', helloCommand)
    cli.set_command('goodbye', goodbyeCommand)

    cli.run()


if __name__ == '__main__':
    main()
