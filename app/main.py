import logging
from fastapi import FastAPI

from .middleware import LoggingContextMiddleware, UserContextFilter
from .routers import auth

logging.basicConfig(format="%(levelname)s %(user_id)s %(message)s")
logging.getLogger().addFilter(UserContextFilter())

app = FastAPI()
app.add_middleware(LoggingContextMiddleware)

app.include_router(auth.router)
