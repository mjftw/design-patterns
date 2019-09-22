
from command import Command, MacroCommand
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


# Concerete Class implimenting Command interface
class AddCommand(Command):
    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self, *args):
        answer = self.reciever.add(*args)

        print(f'{" + ".join(args)} = {answer}')


# Reciever
class Adder:
    def add(self, *args):
        return sum(int(x) for x in args)


def main():
    logHello = Logger('Hello World!')
    logGoodbye = Logger('Goodbye World!')
    adder = Adder()

    helloCommand = LogCommand(logHello)
    goodbyeCommand = LogCommand(logGoodbye)
    addCommand = AddCommand(adder)

    greetingsMacro = MacroCommand(helloCommand, goodbyeCommand)

    cli = CLI()
    cli.set_command('hello', helloCommand)
    cli.set_command('goodbye', goodbyeCommand)
    cli.set_command('add', addCommand)
    cli.set_command('greetings', greetingsMacro)

    cli.run()


if __name__ == '__main__':
    main()
