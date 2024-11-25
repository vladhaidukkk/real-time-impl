from itertools import count

from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Receive, Scope, Send


class SessionManagerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.id_count = count(1)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        if "session_id" not in connection.session:
            connection.session["session_id"] = next(self.id_count)

        await self.app(scope, receive, send)
