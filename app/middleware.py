import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from .core.security import decode_token
from .log_context import user_id_var


class LoggingContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_id_var.set(None)
        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
            try:
                payload = decode_token(token)
                user_id_var.set(payload.get("sub"))
            except Exception:
                pass
        response = await call_next(request)
        return response


class UserContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.user_id = user_id_var.get()
        return True
