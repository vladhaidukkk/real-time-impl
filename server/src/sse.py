import json
from collections import defaultdict
from collections.abc import Generator
from json import JSONDecodeError
from typing import ClassVar

from starlette import status
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse


class ServerSentMessages(HTTPEndpoint):
    """Server-Sent Events (SSE) endpoints for Messages."""

    session_id_to_offset: ClassVar[defaultdict[int, int]] = defaultdict(lambda: 0)
    messages: ClassVar[list[str]] = []

    async def get(self, request: Request) -> StreamingResponse:
        def event_stream() -> Generator[str, None, None]:
            while True:
                session_id = request.session["session_id"]
                offset = self.session_id_to_offset[session_id]
                messages_to_send = self.messages[offset:]

                if messages_to_send:
                    self.session_id_to_offset[session_id] = len(self.messages)
                    yield f"data: {json.dumps(messages_to_send)}\n\n"

        return StreamingResponse(
            event_stream(),
            headers={
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
            },
        )

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
