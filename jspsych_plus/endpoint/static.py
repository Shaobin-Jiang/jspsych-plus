import os

from starlette.requests import Request
from starlette.responses import FileResponse, Response

from ..jspsych import Jspsych


def static(request: Request) -> Response:
    """
    Matches the path parameter with these file patterns one by one:

    - {file.path}
    - {file:path}.html
    - {file.path}/index.html

    If these do not match, 404 will be returned.
    """
    app: Jspsych = request.app

    path: str = os.path.join(app.static_dir, request.path_params["file"])

    def _response(path: str) -> FileResponse | None:
        if os.path.exists(path) and os.path.isfile(path):
            return FileResponse(path)

    return (
        _response(path)
        or _response(f"{path}.html")
        or _response(os.path.join(path, "index.html"))
        or Response(status_code=404)
    )
