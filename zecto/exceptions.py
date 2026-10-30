from __future__ import annotations

import sys
from typing import Any

_STATUS_NAMES = {
    400: "Bad Request",
    401: "Authentication Error",
    403: "Permission Denied",
    404: "Not Found",
    409: "Conflict",
    422: "Validation Error",
    429: "Rate Limit Exceeded",
    502: "Upstream Error",
}

_RED = "\033[91m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_RESET = "\033[0m"


def _use_color() -> bool:
    return hasattr(sys.stderr, "isatty") and sys.stderr.isatty()


def _c(text: str, *codes: str) -> str:
    if not _use_color():
        return text
    return "".join(codes) + text + _RESET


class ZectoError(Exception):
    pass


class InvalidRequestError(ZectoError):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)

    def __str__(self) -> str:
        header = _c("Invalid Request", _BOLD, _RED)
        return f"\n\n{header}\n{self.detail}\n"


class APIConnectionError(ZectoError):
    def __init__(self, message: str = "Could not connect to the Zecto API") -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        header = _c("Connection Error", _BOLD, _RED)
        body = f"{self.message}\nCould not reach the Zecto API. Check your network or base_url."
        return f"\n\n{header}\n{body}\n"


class APIError(ZectoError):
    def __init__(
        self,
        status_code: int,
        detail: str,
        body: dict[str, Any] | None = None,
        method: str | None = None,
        path: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.body = body or {}
        self.method = method
        self.path = path
        super().__init__(f"[{status_code}] {detail}")

    def __str__(self) -> str:
        name = _STATUS_NAMES.get(self.status_code, "API Error")
        header = _c(f"{name} [{self.status_code}]", _BOLD, _RED)
        lines = ["", "", header, self.detail]
        if self.method and self.path:
            lines.append(_c(f"Request: {self.method} {self.path}", _DIM))
        lines.append("")
        return "\n".join(lines)


class ValidationError(APIError):
    pass


class AuthenticationError(APIError):
    pass


class PermissionDeniedError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ConflictError(APIError):
    pass


class RateLimitError(APIError):
    pass


class UpstreamError(APIError):
    pass


class ServerError(APIError):
    pass


_STATUS_MAP = {
    400: ValidationError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitError,
    502: UpstreamError,
}


def error_for_status(
    status_code: int,
    detail: str,
    body: dict[str, Any] | None = None,
    method: str | None = None,
    path: str | None = None,
) -> APIError:
    cls = _STATUS_MAP.get(status_code)
    if cls is None:
        cls = ServerError if status_code >= 500 else APIError
    return cls(status_code, detail, body, method=method, path=path)
