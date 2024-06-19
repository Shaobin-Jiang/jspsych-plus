import os
import shutil
import sys
from typing import Any, Callable, Dict

from .. import __basedir__, __version__


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


def create_project(name: str = "jspsych-project", path: str = "", *_) -> None:
    """
    Creates a project by `name` at `path`.

    The parameter `path` can be either relative or absolute. By default, it is
    empty, which means that the project directory will be created under the
    current path.
    """
    cwd: str = os.getcwd()
    if os.path.isabs(path):
        project_path: str = os.path.join(path, name)
    else:
        project_path: str = os.path.abspath(os.path.join(cwd, path, name))

    if os.path.exists(project_path):
        if len(os.listdir(project_path)) > 0:
            print(f"Cannot create project as {project_path} is not empty.")
            return
    else:
        os.makedirs(project_path)

    template_dir: str = os.path.join(__basedir__, "template")

    # The variables to be replaced in each file, relative to the template dir
    replace_var: Dict[str, Dict[str, str]] = {
        "index.html": {
            "project_name": name,
        },
        "src/scripts/main.js": {
            "project_name": name,
        },
    }

    shutil.copytree(
        template_dir,
        project_path,
        dirs_exist_ok=True,
    )

    for file in replace_var:
        var_map = replace_var[file]
        target_file: str = os.path.join(project_path, file)

        with open(target_file, mode="r") as fid:
            content: str = fid.read()
            for key in var_map:
                content = content.replace(f"{{{{ {key} }}}}", var_map[key])

        with open(target_file, mode="w") as fid:
            fid.write(content)

    print(f"Created project {name} at {project_path}.")


# Map between command name and the command itself
NAME_COMMAND_MAP: dict[str, Callable[..., Any]] = {
    "-h": print_help,
    "help": print_help,
    "new": create_project,
}
