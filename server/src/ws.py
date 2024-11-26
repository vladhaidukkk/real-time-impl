from typing import ClassVar

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket


class WebSocketMessages(WebSocketEndpoint):
    encoding = "json"

    clients: ClassVar[set[WebSocket]] = set()
    messages: ClassVar[list[str]] = []

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

        self.clients.add(websocket)
        await websocket.send_json({"messages": self.messages})

    async def on_receive(self, websocket: WebSocket, data: dict) -> None:
        try:
            message = data["message"]
        except KeyError:
            await websocket.send_json({"message": "Message not provided"})
        else:
            if message:
                self.messages.append(message)
                for client in self.clients:
                    await client.send_json({"messages": [message]})
            else:
                await websocket.send_json({"message": "Message cannot be empty"})

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        self.clients.remove(websocket)
