from asyncio import sleep
from collections import defaultdict
from json import JSONDecodeError
from time import time
from typing import ClassVar

from starlette import status
from starlette.datastructures import Address
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse


class LongPollingMessages(HTTPEndpoint):
    TIMEOUT: float = 30.0
    DELAY: float = 1.0

    # Mapping of clients to messages offset.
    clients: ClassVar[defaultdict[Address, int]] = defaultdict(lambda: 0)
    messages: ClassVar[list[str]] = []

    async def get(self, request: Request) -> JSONResponse:
        start_time = time()

        while time() - start_time < self.TIMEOUT:
            messages_offset = self.clients[request.client]
            messages_to_send = self.messages[messages_offset:]

            if messages_to_send:
                self.clients[request.client] = len(self.messages)
                return JSONResponse({"messages": messages_to_send})

            # Non-blocking sleep, to continue processing new requests.
            await sleep(self.DELAY)

        return JSONResponse({"message": "Request timed out"}, status.HTTP_504_GATEWAY_TIMEOUT)

    async def post(self, request: Request) -> JSONResponse:
        try:
            data = await request.json()
            message = data["message"]
        except JSONDecodeError:
            resp_message = "Invalid JSON data"
            resp_code = status.HTTP_400_BAD_REQUEST
        except KeyError:
            resp_message = "Message not provided"
            resp_code = status.HTTP_400_BAD_REQUEST
        else:
            if message:
                self.messages.append(message)
                resp_message = "Message accepted"
                resp_code = status.HTTP_201_CREATED
            else:
                resp_message = "Message cannot be empty"
                resp_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        return JSONResponse({"message": resp_message}, status_code=resp_code)
