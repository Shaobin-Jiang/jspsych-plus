import inspect
import os
from typing import Any, Callable, Mapping, Sequence

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute, Route
from starlette.types import ExceptionHandler


class Jspsych(Starlette):
    """
    Creates a jsPsych application instance with the parameters below:

    - debug: whether debug tracebacks should be returned on errors
    - routes: list of routes to serve incoming HTTP and WebSocket requests.
    - middleware: list of middleware to run for every request.
    - exception_handlers: mapping of integer status codes or exception class types onto callables which handle the
      exceptions. See https://www.starlette.io/exceptions/ for more information.
    - on_startup / on_shutdown: list of callables to run on application startup / shutdown.
      These callables do not take any argument and can either be standard functions or async functions.
    - pages_dir: directory where static files like HTML pages and JavaScript codes are placed.

    As jspsych-plus is based on Starlette, for those familiar with Starlette, you might notice the missing of the
    `lifespan` parameter. We choose not to include it because once we decide to give it a default value, it is then ill-
    suited for further customization.
    """

    def __init__(
        self,
        debug: bool = True,
        routes: Sequence[BaseRoute] | None = None,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, ExceptionHandler] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        static_dir: str | None = None,
    ):
        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )

        # Gets the directory of the file from which the Jspsych class is instantiated and use that path as the base dir.
        self._base_dir: str = os.path.dirname(inspect.stack()[1].filename)

        self.static_dir: str = static_dir or os.path.join(self._base_dir, "pages")

        self._add_default_route()

    def _add_default_route(self) -> None:
        from .endpoint.static import static

        self.router.routes.extend(
            [
                Route("/{file:path}", static, methods=["GET"]),
            ]
        )
