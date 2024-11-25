from asyncio import sleep
from json import JSONDecodeError
from time import time
from typing import ClassVar

from starlette import status
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse


class LongPollingMessages(HTTPEndpoint):
    TIMEOUT: float = 30.0
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
            self.messages_queue.append(message)
            resp_message = "Message accepted"
            resp_code = status.HTTP_201_CREATED

        return JSONResponse({"message": resp_message}, status_code=resp_code)
