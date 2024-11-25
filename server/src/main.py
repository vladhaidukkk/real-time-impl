from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route

from .long_polling import LongPollingMessages

routes = [Route("/lp/messages", LongPollingMessages)]

middleware = [Middleware(CORSMiddleware, allow_origins=["*"])]

app = Starlette(routes=routes, middleware=middleware)
