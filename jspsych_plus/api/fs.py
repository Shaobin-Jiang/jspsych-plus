import json
import os

from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response


def read_file(request: Request) -> Response:
    """
    Reads the content of a file via a GET request. The request should have a
    query parameter:

    - path: the path to the file
    """
    from ..applications.jspsych import Jspsych

    app: Jspsych = request.app

    base_path: str = os.path.abspath(app.data_dir)
    path: str = parse_path(base_path, request.query_params["path"])

    if not os.path.exists(path) or not os.path.isfile(path):
        return Response(content="Non existent file", status_code=403)

    if not path.startswith(base_path):
        return Response(content="Permission denied", status_code=403)

    return FileResponse(path=path)


async def write_file(request: Request) -> Response:
    """
    Writes content to the given file via a POST request. The request body should
    contain:

    - path: path to the file
    - content: the content to write in the file
    """
    from ..applications.jspsych import Jspsych

    app: Jspsych = request.app

    base_path: str = os.path.abspath(app.data_dir)

    body = json.loads((await request.body()).decode())
    path: str = parse_path(base_path, body["path"])
    content: str = body["content"]

    if not path.startswith(base_path):
        return Response(content="Permission denied", status_code=403)

    with open(path, mode="w") as fid:
        fid.write(content)

    return Response(status_code=200)


def remove_file(request: Request):
    # TODO: implement this
    pass


def tree(request: Request) -> Response:
    """
    Gets the file tree via a GET request. The returned response is basically the
    same as the result of `os.walk`, with a list of tuples made up with `root`,
    `directories` and `files`. The request should have a query parameter:

    - path: the path to the directory
    """
    from ..applications.jspsych import Jspsych

    app: Jspsych = request.app

    base_path: str = os.path.abspath(app.data_dir)
    path: str = parse_path(base_path, request.query_params["path"])

    if not os.path.exists(path) or not os.path.isdir(path):
        return Response(content="Non existent path", status_code=403)

    if not path.startswith(base_path):
        return Response(content="Permission denied", status_code=403)

    walk_result: list[tuple[str, list[str], list[str]]] = []
    for root, dirs, files in os.walk(path):
        walk_result.append((root, dirs, files))

    return JSONResponse(content=json.dumps(walk_result))

def mkdir(request: Request):
    # TODO: implement this
    pass


def rmdir(request: Request):
    # TODO: implement this
    pass


def parse_path(base_path: str, path: str) -> str:
    while path.startswith("/"):
        path = path[1:]

    return os.path.abspath(os.path.join(base_path, path))
