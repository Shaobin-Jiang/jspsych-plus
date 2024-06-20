from typing import Dict
from .. import __version__


def print_help(commands: Dict[str, str], *_) -> None:
    """
    Prints a brief introduction of the project and the management commands.

    For example:

    print_help({"help": "Prints this help info"})

    would add help info for "jspsych help" at the end of the help string.

    By default, no help for any command is added.
    """
    help_str_list: list[str] = [
        "",
        f"Welcome to jspsych-plus {__version__}.",
        "Usage: jspsych <command> [<args>]",
        "",
        "Available commands are listed below:",
        "",
    ]

    max_cmd_len: int = 7 # same length as "Command"
    for command in commands:
        entry: str = f"jspsych {command}"
        max_cmd_len = max(len(entry), max_cmd_len)
    max_cmd_len += 4 # leave 4 blank spaces after

    help_str_list.append(f"Command{' ' * (max_cmd_len - 7)}Description")
    help_str_list.append(f"-------{' ' * (max_cmd_len - 7)}-----------")
    for command in commands:
        entry: str = f"jspsych {command}"
        entry = f"{entry}{' ' * (max_cmd_len - len(entry))}{commands[command]}"
        help_str_list.append(entry)

    print("\n".join(help_str_list))
