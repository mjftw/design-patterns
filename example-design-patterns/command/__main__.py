
from .command import MacroCommand
from .commands import AddCommand, Adder, LogCommand, Logger
from .cli import CLI


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
