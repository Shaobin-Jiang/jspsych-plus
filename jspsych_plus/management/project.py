import os
import shutil
from typing import Dict

from .. import __basedir__, __version__


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
        "requirements.txt": {
            "version": __version__,
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
