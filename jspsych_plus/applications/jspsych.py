import inspect
import os
from typing import Any, Callable, Mapping, Sequence

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute, Mount, Route, WebSocketRoute
from starlette.types import ExceptionHandler

from ..api.channel import VarPool, establish_var_channel
from ..api.static import static
from ..api.fs import read_file, tree, write_file


class Jspsych(Starlette):
    """
    Creates a jsPsych application instance with the parameters below:

    - debug: whether debug tracebacks should be returned on errors; true by
      default
    - routes: list of routes to serve incoming HTTP and WebSocket requests.
    - middleware: list of middleware to run for every request.
    - exception_handlers: mapping of integer status codes or exception class
      types onto callables which handle the exceptions.
      See https://www.starlette.io/exceptions/ for more information.
    - on_startup / on_shutdown: list of callables to run on application
      startup / shutdown.
      These callables do not take any argument and can either be standard
      functions or async functions.

    As jspsych-plus is based on Starlette, for those familiar with Starlette,
    you might notice the missing of the `lifespan` parameter. We choose not to
    include it because once we decide to give it a default value, it is then
    ill-suited for further customization.
    """

    def __init__(
        self,
        debug: bool = True,
        routes: Sequence[BaseRoute] | None = None,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, ExceptionHandler] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
    ):
        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )

        self._base_dir: str = os.path.dirname(inspect.stack()[1].filename)
        self.data_dir: str = os.path.join(self._base_dir, "data")
        self.static_dir: str = os.path.join(self._base_dir, "pages")

        self.var_pool = VarPool()
        self._add_default_route()

    def _add_default_route(self) -> None:
        self.router.routes.extend(
            [
                WebSocketRoute("/_channel", establish_var_channel),
                Mount("/fs", routes=[
                    Route("/read", read_file, methods=["GET"]),
                    Route("/write", write_file, methods=["POST"]),
                    Route("/tree", tree, methods=["GET"]),
                ]),
                Route("/{file:path}", static, methods=["GET"]),
            ]
        )
