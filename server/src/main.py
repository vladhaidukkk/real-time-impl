from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route

from .config import SECRET_KEY
from .long_polling import LongPollingMessages
from .session import SessionManagerMiddleware
from .sse import ServerSentMessages
from .ws import WebSocketMessages

routes = [
    Route("/lp/messages", LongPollingMessages),
    Route("/sse/messages", ServerSentMessages),
    Route("/ws/messages", WebSocketMessages),
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:3000"],
        allow_methods=["*"],
        allow_credentials=True,
    ),
    Middleware(SessionMiddleware, secret_key=SECRET_KEY),
    Middleware(SessionManagerMiddleware),
]

app = Starlette(routes=routes, middleware=middleware)
