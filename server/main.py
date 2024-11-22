from asyncio import sleep
from time import time
from typing import ClassVar

from starlette import status
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


class LongPollingMessages(HTTPEndpoint):
    TIMEOUT: float = 10.0
    DELAY: float = 5.0

    messages_queue: ClassVar[list[str]] = []

    async def get(self, request: Request) -> JSONResponse:
        start_time = time()

        while time() - start_time < self.TIMEOUT:
            if self.messages_queue:
                messages_to_send = self.messages_queue.copy()
                self.messages_queue.clear()
                return JSONResponse({"messages": messages_to_send})

            # Non-blocking sleep, to continue processing new requests.
            await sleep(self.DELAY)

        return JSONResponse({"message": "Request timed out"}, status.HTTP_504_GATEWAY_TIMEOUT)

    async def post(self, request: Request) -> JSONResponse:
        body = await request.body()
        self.messages_queue.append(body.decode())
        return JSONResponse({"message": "Message sent"})


routes = [Route("/messages", LongPollingMessages)]

app = Starlette(routes=routes)
