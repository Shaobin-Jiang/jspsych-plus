import sys
from typing import Any, Callable

from .. import __version__


def exec_from_cmd() -> None:
    """
    The function that gets executed when the user runs the `jspsych` command
    from the command line. It runs corresponding tasks based on the command line
    parameters.
    """
    argv: list[str] = sys.argv[1:]

    if len(argv) == 0:
        print_help()
        return

    command_name: str = argv[0].lower()
    if command_name not in NAME_COMMAND_MAP:
        print_help()
        return

    command: Callable[..., Any] = NAME_COMMAND_MAP[command_name]
    params: list[str] = argv[1:]
    command(*params)


def print_help(*_) -> None:
    """
    Prints a brief introduction of the project and the management commands.
    """
    print(
        "\n".join(
            [
                "",
                f"Welcome to jspsych-plus {__version__}.",
                "Usage: jspsych <command> [<args>]",
                "",
                "Available commands are listed below:",
                "",
                "Command                      Description",
                "-------                      -----------",
                "jspsych help                 Prints this help info.",
                "jspsych new [name] [path]    Creates a new project.",
            ]
        )
    )


# Map between command name and the command itself
NAME_COMMAND_MAP: dict[str, Callable[..., Any]] = {
    "-h": print_help,
    "help": print_help,
}
