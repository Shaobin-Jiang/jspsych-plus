from typing import Any, Callable, Dict
from starlette.websockets import WebSocket


class VarPool:
    """
    Creates a variable pool. Changes made on the variables inside this pool from
    the server will be forwarded to the client side.
    """

    def __init__(self):
        self._var_pool: Dict[str, Any] = {}
        self._websockets: list[WebSocket] = []

    async def set(
        self,
        var: str,
        value: Any | None = None,
        func: Callable[[Any], Any] | None = None,
    ) -> None:
        """
        Sets the value of a variable. If that value does not exists, it is then
        added to the pool.

        One can either directly specifies the value of a variable or pass a
        callable to deal with an existing variable. The latter is better suited
        for lists or objects and has a higher priority, which means that should
        both a value and a callable is passed to the method, the callable will
        be used.
        """
        if func == None:
            self._var_pool[var] = value
        else:
            if var not in self._var_pool:
                return

            func(self._var_pool[var])

        await self._send(var)

    async def add_socket(self, websocket: WebSocket) -> None:
        """
        Add a websocket connection that will be notified every once modification
        to a variable is made. Upon adding this websocket, the current variable
        pool will be sent to it.
        """
        self._websockets.append(websocket)
        await websocket.send_json(self._var_pool)

    async def _send(self, var: str) -> None:
        # TODO: process complex data type like sequences before sending them
        await self._send_json({var: self._var_pool[var]})

    async def _send_json(self, content: dict) -> None:
        for websocket in self._websockets:
            await websocket.send_json(content)


async def establish_var_channel(websocket: WebSocket) -> None:
    """
    Establishes a variable channel between the client and the server.
    """
    await websocket.accept()

    # import here to prevent cirular import
    from ..applications.jspsych import Jspsych

    app: Jspsych = websocket.app
    await app.var_pool.add_socket(websocket)
