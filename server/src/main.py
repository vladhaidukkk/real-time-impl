from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route

from .config import SECRET_KEY
from .long_polling import LongPollingMessages

routes = [Route("/lp/messages", LongPollingMessages)]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:3000"],
        allow_methods=["*"],
        allow_credentials=True,
    ),
    Middleware(SessionMiddleware, secret_key=SECRET_KEY),
]

app = Starlette(routes=routes, middleware=middleware)
