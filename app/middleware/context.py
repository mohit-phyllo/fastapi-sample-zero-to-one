from datetime import datetime
from contextvars import ContextVar
from typing import Optional
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

CORRELATION_ID_CTX_KEY = "correlation_id"
TENANT_APP_ID_CTX_KEY = "tenant_app_id"
X_FORWARDED_FOR_CTX_KEY = "X-Forwarded-For"
START_TIME_CTX_KEY = "start_time"
END_TIME_CTX_KEY = "end_time"
RESPONSE_DURATION_CTX_KEY = "response_duration"

HEADER_REQUEST_ID = 'Request-Id'


_correlation_id_ctx_var: ContextVar[Optional[str]] = ContextVar(CORRELATION_ID_CTX_KEY, default=None)
_tenant_app_id_ctx_var: ContextVar[Optional[str]] = ContextVar(TENANT_APP_ID_CTX_KEY, default=None)
_x_forwarded_for_ctx_var: ContextVar[Optional[str]] = ContextVar(X_FORWARDED_FOR_CTX_KEY, default=None)
_start_time_ctx_var: ContextVar[Optional[datetime]] = ContextVar(START_TIME_CTX_KEY, default=None)
_end_time_ctx_var: ContextVar[Optional[datetime]] = ContextVar(END_TIME_CTX_KEY, default=None)
_response_duration_ctx_var: ContextVar[Optional[int]] = ContextVar(RESPONSE_DURATION_CTX_KEY, default=None)


def get_x_forwarded_for() -> Optional[str]:
    return _x_forwarded_for_ctx_var.get() if _x_forwarded_for_ctx_var else None


def get_correlation_id() -> Optional[str]:
    return _correlation_id_ctx_var.get() if _correlation_id_ctx_var else None


def get_tenant_app_id() -> Optional[str]:
    return _tenant_app_id_ctx_var.get() if _tenant_app_id_ctx_var else None


def get_start_time() -> Optional[datetime]:
    return _start_time_ctx_var.get() if _start_time_ctx_var else None


def get_end_time() -> Optional[datetime]:
    return _end_time_ctx_var.get() if _end_time_ctx_var else None


def get_response_duration() -> Optional[int]:
    return _response_duration_ctx_var.get() if _response_duration_ctx_var else None


class RequestContextLogMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        _correlation_id_ctx_var.set(request.headers.get("Correlation-Id", str(uuid4())))
        correlation_id = get_correlation_id()
        start_time = datetime.utcnow()
        response: Response = await call_next(request)
        end_time = datetime.utcnow()
        if correlation_id is not None:
            response.headers[HEADER_REQUEST_ID] = correlation_id
        response_duration = end_time - start_time
        _start_time_ctx_var.set(start_time)
        _end_time_ctx_var.set(end_time)
        _response_duration_ctx_var.set(response_duration.microseconds)
        return response

